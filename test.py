import traceback
import warnings
from pathlib import Path
import pandas as pd
from typing import List
from sqlalchemy import select, Table, MetaData, text, create_engine
import oracledb
oracledb.init_oracle_client()
import functools


cdb_engine_L1W = create_engine("oracle+oracledb://GRWMGR:GRWMGR_2636@10.10.17.62:1521/?service_name=mesarcdb",
                               pool_size=2,
                               )
cdb_engine_L2W = create_engine("oracle+oracledb://GRWMGR:GRWMGR_2636@10.100.10.44/?service_name=l2mesdb_dg",
                               pool_size=2,
                               )


def check_equal(value_a: float, value_b: float) -> bool:
    if abs(value_a - value_b) < 0.0001:
        return True
    else:
        return False


def get_cdb_engine(virtual_factory: str):
    if virtual_factory == 'L1W':
        return cdb_engine_L1W
    else:
        return cdb_engine_L2W


@functools.cache
def get_wafer_current_status_cross_factory(wafer_id) -> pd.DataFrame:
    sql = text(rf"""
    SELECT * FROM MESMGR.MWIPSLTSTS
    WHERE 1 = 1
    AND SUBLOT_ID = '{wafer_id}'
    """)
    df_list = []
    for v_factory in ['L2W', 'L1W']:
        with get_cdb_engine(v_factory).connect() as l1w_connection:
            df = pd.read_sql(sql, con=l1w_connection)
            if len(df) > 0:
                df_list.append(df)

    current_status = pd.concat(df_list).sort_values(by='last_hist_seq', ascending=False).iloc[0, :]
    if current_status['factory'] in ['WE1', 'GR1']:
        current_status['virtual_factory'] = 'L1W'
    elif current_status['factory'] in ['L2C', 'L2W']:
        current_status['virtual_factory'] = 'L2W'
    return current_status


@functools.cache
def get_ingot_tp_df_cross_factory(ingot_id, IE2_char_id_root):
    assert IE2_char_id_root[:4] not in ['1500', '2900'], 'IE2_char_id_root should not contain operation'
    tp_df_list = []
    for factory in ['L2W', 'L1W']:
        with get_cdb_engine(factory).connect() as cc:
            sql = text(rf"""
        SELECT A.SUBLOT_ID, B.UPDATE_TIME, B.UPDATED_BY, B.EXT_MV, B.SPEC_ID, A.SUBLOT_CMF_9 FROM MESMGR.MWIPSLTSTS A
          JOIN SPCMGR.TQS_SUMMARY_DATA B
        ON B.USR_CMF_07 LIKE A.SUBLOT_ID || '%'
        WHERE 1 =1
        AND A.SUBLOT_CMF_1 = '{ingot_id}00'
        AND (B.SPEC_ID LIKE '2900-{IE2_char_id_root}__'
        OR B.SPEC_ID LIKE '1500-{IE2_char_id_root}__')
            """)

            _tp_df = pd.read_sql(sql, con=cc)
            if len(_tp_df) == 0:
                continue
            tp_df_list.append(_tp_df)
    tp_df = pd.concat(tp_df_list).sort_values(
        by=['update_time'], ascending=False).groupby(by=['sublot_id', 'spec_id'], as_index=False).first()
    tp_df = tp_df.sort_values(by=['update_time'])
    tp_df = tp_df.drop_duplicates(subset=['sublot_id'], keep='last')
    position_list = []
    format_wafer_id_list = []
    for _, _row_data in tp_df.iterrows():
        wafer_raw_id = _row_data['sublot_id']
        position_str = _row_data['sublot_cmf_9']
        position_list.append(float(position_str) * 10)
        format_wafer_id_list.append(wafer_raw_id.strip())

    new_df = pd.DataFrame({
        'tp_id': format_wafer_id_list,
        'spec_id': tp_df['spec_id'],
        'position': position_list,
        'update_time': tp_df['update_time'],
        'updated_by': tp_df['updated_by'],
        'value': tp_df['ext_mv'],
    })
    # columns: tp_id, spec_id, position, update_time, updated_by, value
    return new_df


@functools.cache
def get_IE2_data(group_id, char_id, v_factory):
    sql = text(rf"""
        SELECT AVG_DATA, CMF_20  FROM MESMGR.CSAMSPCDAT A
          WHERE A.CHAR_ID = '{char_id}'
          AND A.SEGMENT_LOT_ID = '{group_id}'
        """)
    with get_cdb_engine(v_factory).connect() as c:
        result_df = pd.read_sql(sql, con=c)
        result_df.sort_values(by='cmf_20', ascending=False, inplace=True)
        if len(result_df) == 0:
            return None
        else:
            return result_df.iloc[0, 0]


def get_tp_info(ingot_used_tp_df, used_char_value) -> pd.Series:
    for _row_index, row_data in ingot_used_tp_df.iterrows():
        if check_equal(row_data['value'], used_char_value):
            return row_data


def get_sample_data(wafer_id: str, char_id_root: str):
    # char_id is like 2900-CTRRESTE
    # char_id_root = char_id[5:-2]  delete 2900- and se/te
    se_char_id = rf'2900-{char_id_root}SE'
    te_char_id = rf'2900-{char_id_root}TE'
    wafer_id = wafer_id.strip()
    wafer_status = get_wafer_current_status_cross_factory(wafer_id)
    virtual_factory = wafer_status['virtual_factory']
    group_id = wafer_status['sublot_cmf_16']
    if group_id == ' ':
        group_id = wafer_id[:8]

    se_char_data = get_IE2_data(group_id, se_char_id, virtual_factory)
    te_char_data = get_IE2_data(group_id, te_char_id, virtual_factory)

    if se_char_data is None:
        raise ValueError(f'{wafer_id} {se_char_id} is None')

    if te_char_data is None:
        raise ValueError(f'{wafer_id} {te_char_id} is None')

    ingot_sample_df = get_ingot_tp_df_cross_factory(wafer_status['sublot_cmf_1'][:-2], char_id_root)
    se_tp_info = get_tp_info(ingot_sample_df, se_char_data)
    te_tp_info = get_tp_info(ingot_sample_df, te_char_data)

    return se_tp_info, te_tp_info


def get_sample_wafer_main(wafer_id_list: List[str], wafer_char_id_root: str, output_path=r'P:\963\tp_sample.xlsx'):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    columns_list = ['wafer_id', 'se_tp_id', 'se_tp_value', 'se_tp_position', 'se_update_time',
                    'te_tp_id', 'te_tp_value', 'te_tp_position', 'te_update_time']
    data_list_list = []
    for _index, wafer_id in enumerate(wafer_id_list):
        try:
            se_tp_info, te_tp_info = get_sample_data(wafer_id, wafer_char_id_root)
            data_list_list.append([wafer_id,
                                   se_tp_info['tp_id'], se_tp_info['value'], se_tp_info['position'], se_tp_info['update_time'],
                                   te_tp_info['tp_id'], te_tp_info['value'], te_tp_info['position'], te_tp_info['update_time']])
        except Exception:
            print(traceback.format_exc())
            pass
    df = pd.DataFrame(data_list_list, columns=columns_list)
    df.to_excel(output_path, index=False)
    print(f'excel output finished at {output_path}')


if __name__ == "__main__":
    wafer_id_list  = ['E36010B20301', 'E36010B20302', 'E36010B20303']
    wafer_char_id_root = 'CTRRES'
    get_sample_wafer_main(wafer_id_list, wafer_char_id_root)