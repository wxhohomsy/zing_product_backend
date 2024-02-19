import pandas as pd
from typing import Dict, Tuple
from sqlalchemy import text
from sqlalchemy.engine.row import RowMapping
from cachetools import cached, TTLCache
from zing_product_backend.app_db.connections import l1w_db_engine, l2w_db_engine
from zing_product_backend.core.common_type import *
from zing_product_backend.core import common
from zing_product_backend import settings
from zing_product_backend.global_utils import mes_db_utils


t_mapping_or_none = Union[RowMapping, None]
t_float_or_none = Union[float, None]


class NotFindInDBError(Exception):
    pass


def generate_spec_like_query(spec_col_name: str, oper_id_tuple: Tuple[str]):
    query_parts = [f"{spec_col_name} like '{oper_id}-%'" for oper_id in oper_id_tuple]
    query = " or ".join(query_parts)
    return f"({query})"


def get_cdb_engine(virtual_factory: common.VirtualFactory):
    if virtual_factory == common.VirtualFactory.L1W:
        return l1w_db_engine
    elif virtual_factory == common.VirtualFactory.L2W:
        return l2w_db_engine
    else:
        raise ValueError(f"factory {virtual_factory} is not supported")


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_available_oper_id_list(start_oper: str, end_oper_str: str, virtual_factory: common.VirtualFactory) -> List[str]:
    cdb_engine = get_cdb_engine(virtual_factory)
    with cdb_engine.connect() as c:
        sql = text(f"select distinct oper from MESMGR.MWIPFLWOPR where oper >= '{start_oper}' "
                   f"and oper <= '{end_oper_str}'")
        data = c.execute(sql).fetchall()
        oper_id_list = [d[0] for d in data]
        oper_id_list.sort()
        return oper_id_list


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_sublot_sts_cross_factory(sublot_id: str) -> RowMapping:
    return_data = None
    virtual_factory = None
    for v_factory in [common.VirtualFactory.L1W, common.VirtualFactory.L2W]:
        with get_cdb_engine(v_factory).connect() as c:
            sql = text(f"select * from MESMGR.MWIPSLTSTS where SUBLOT_ID = '{sublot_id}'")
            data = c.execute(sql).fetchone()
            if data:
                if return_data is None:
                    return_data = data
                    virtual_factory = v_factory.value
                else:
                    # chose newest record
                    if data._mapping['last_tran_time'] > return_data._mapping['last_tran_time']:
                        return_data = data
                        virtual_factory = v_factory.value

    if return_data is None:
        raise NotFindInDBError(sql)
    else:
        data_dict = dict(return_data._mapping)
        data_dict['virtual_factory'] = virtual_factory
        return data_dict


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_sublot_sts_by_lot_id(lot_id: str, virtual_factory: common.VirtualFactory) -> pd.DataFrame:
    cdb_engine = get_cdb_engine(virtual_factory)
    with cdb_engine.connect() as c:
        sql = text(f"select * from MESMGR.MWIPSLTSTS where LOT_ID = '{lot_id}' ")
        df = pd.read_sql(sql, c)
    return df


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_sublot_sts_by_wafering_segment_id_cross_factory(wafering_segment_id: str) -> pd.DataFrame:
    df_list = []
    param = {
        'wafering_segment_id': wafering_segment_id,
    }
    for virtual_factory in [common.VirtualFactory.L1W, common.VirtualFactory.L2W]:
        with get_cdb_engine(virtual_factory).connect() as c:
            sql = text(f"""select * from MESMGR.MWIPSLTSTS where sublot_cmf_2 = :wafering_segment_id 
                       """)
            df = pd.read_sql(sql, c, params=param)
            df_list.append(df)

    all_empty = all([len(df) == 0 for df in df_list])
    if all_empty:
        data_df = df_list[0]
    else:
        not_empty_df_list = [df for df in df_list if len(df) > 0]
        data_df = pd.concat(not_empty_df_list)

    data_df = data_df.sort_values(by=['last_tran_time'], ascending=False
                                  ).drop_duplicates(subset=['sublot_id'], keep='first').sort_values(
        by=['sublot_id'], ignore_index=True)
    return data_df


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_sublot_sts_by_ingot_id_cross_factory(ingot_id: str) -> pd.DataFrame:
    df_list = []
    param = {
        'ingot_id': ingot_id + '00',
    }
    for virtual_factory in [common.VirtualFactory.L1W, common.VirtualFactory.L2W]:
        with get_cdb_engine(virtual_factory).connect() as c:
            sql = text(f"""select * from MESMGR.MWIPSLTSTS where sublot_cmf_1 = :ingot_id
                        """)
            df = pd.read_sql(sql, c, params=param)
            df_list.append(df)

    all_empty = all([len(df) == 0 for df in df_list])
    if all_empty:
        data_df = df_list[0]
    else:
        not_empty_df_list = [df for df in df_list if len(df) > 0]
        data_df = pd.concat(not_empty_df_list)

    data_df = data_df.sort_values(by=['last_tran_time'], ascending=False
                                  ).drop_duplicates(subset=['sublot_id'], keep='first').sort_values(
        by=['sublot_id'], ignore_index=True)
    return data_df


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_lot_sts(lot_id: str, virtual_factory: common.VirtualFactory) -> RowMapping:
    cdb_engine = get_cdb_engine(virtual_factory)
    with cdb_engine.connect() as c:
        sql = text(f"select * from MESMGR.MWIPLOTSTS where LOT_ID = '{lot_id}'")
        data = c.execute(sql).fetchone()
        if data is None:
            raise NotFindInDBError(sql)
        else:
            return data._mapping


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_lot_sts_by_oper_id(oper_id: str, virtual_factory: common.VirtualFactory) -> pd.DataFrame:
    cdb_engine = get_cdb_engine(virtual_factory)
    with cdb_engine.connect() as c:
        sql = text(f"select lot_id, oper, qty_1, mat_id, flow, oper_in_time, last_tran_time"
                   f" from MESMGR.MWIPLOTSTS where OPER = '{oper_id}'"
                   f"and lot_del_flag != 'Y'")
        df = pd.read_sql(sql, c)
    return df


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_lot_sts_by_oper_range(start_oper_id: str,  end_oper_id: str, virtual_factory: common.VirtualFactory
                               ) -> pd.DataFrame:
    cdb_engine = get_cdb_engine(virtual_factory)
    with cdb_engine.connect() as c:
        sql = text(f"select lot_id, oper, qty_1, mat_id, flow, oper_in_time, last_tran_time"
                   f" from MESMGR.MWIPLOTSTS where OPER >= '{start_oper_id}' and OPER <= '{end_oper_id}'"
                   f"and lot_del_flag != 'Y'")
        df = pd.read_sql(sql, c)
    return df


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_growing_segment_id_cross_factory(wafering_segment_id: str):
    sql = text(
        rf"""
        SELECT LOT_ID FROM MESMGR.CGRWCONCRP
        WHERE 1 = 1
        AND CROP_CMF_2 = '{wafering_segment_id}'
        AND LOT_ID NOT LIKE '______00'
        """
    )
    growing_segment_id = wafering_segment_id
    for virtual_factory in [common.VirtualFactory.L1W, common.VirtualFactory.L2W]:
        with get_cdb_engine(virtual_factory).connect() as c:
            data_tuple = c.execute(sql).fetchone()
            if data_tuple is not None:
                growing_segment_id = data_tuple[0]
    return growing_segment_id


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_wafering_segment_id_list_cross_factory(growing_segment_id: str) -> List[str]:
    sql = text(rf"""
         SELECT CROP_CMF_2 FROM MESMGR.CGRWCONCRP
         WHERE 1 = 1
         AND LOT_ID = '{growing_segment_id}'
         and length(CROP_CMF_2) > 4
    """)
    cutted_segment_id_set = set()
    for virtual_factory in [common.VirtualFactory.L1W, common.VirtualFactory.L2W]:
        with get_cdb_engine(virtual_factory).connect() as c:
            for data_tuple in c.execute(sql).fetchall():
                cutted_segment_id_set.add(data_tuple[0])

    to_return_list = [growing_segment_id, *cutted_segment_id_set]
    return to_return_list


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_growing_segment_id_list_by_ingot_id_cross_factory(ingot_id: str) -> List[str]:
    sql = text(rf"""
         SELECT CROP_CMF_2 FROM MESMGR.CGRWCONCRP
         WHERE 1 = 1
         AND LOT_ID = '{ingot_id}00'
    """)
    cutted_segment_id_set = set()
    for virtual_factory in [common.VirtualFactory.L1W, common.VirtualFactory.L2W]:
        with get_cdb_engine(virtual_factory).connect() as c:
            for data_tuple in c.execute(sql).fetchall():
                cutted_segment_id_set.add(data_tuple[0])

    return list(cutted_segment_id_set)


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_segment_sample_data_by_operation_id_list(segment_id: str, oper_id_tuple: List[str],
                                                 virtual_factory: common.VirtualFactory) -> pd.DataFrame:
    assert len(segment_id) in settings.SEGMENT_ID_PERMIT_LENGTH, \
        (f"segment_like_id  {segment_id}'s length"
            f" is not in {settings.SEGMENT_ID_PERMIT_LENGTH}")
    cdb_engine = get_cdb_engine(virtual_factory)
    with cdb_engine.connect() as c:
        sql = text(f"""
        SELECT AVG_DATA, CHAR_ID, CMF_20  FROM MESMGR.CSAMSPCDAT A
          WHERE 1 = 1
          AND {generate_spec_like_query('A.CHAR_ID', oper_id_tuple)}
          AND A.SEGMENT_LOT_ID = '{segment_id}'
          order by CMF_20 desc
        """)
        df = pd.read_sql(sql, c)
        df = df.drop_duplicates(subset=['char_id'], keep='first')
        return df


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.MES_STS_CACHE_TIME), info=settings.DEBUG)
def get_unit_latest_spc_data_by_spec_id(unit_id: str, spec_id: str, virtual_factory: common.VirtualFactory) \
        -> t_float_or_none:
    # spc data means data from tqs_summary_data
    sql = text(f"""
      SELECT ext_mv from spcmgr.tqs_summary_data
      where 1 = 1
      and usr_cmf_07 = '{unit_id}'
      and spec_id = '{spec_id}'
      order by sys_time desc
    """)
    with get_cdb_engine(virtual_factory).connect() as c:
        data = c.execute(sql).fetchone()
        if data is None:
            return None
        else:
            return data[0]


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.SPC_DATA_CACHE_TIME), info=settings.DEBUG)
def get_segment_sample_data_by_char_id(segment_like_id: str, char_id: str,
                                       virtual_factory: common.VirtualFactory) -> (
        t_mapping_or_none):
    assert len(segment_like_id) in settings.SEGMENT_ID_PERMIT_LENGTH, \
        (f"segment_like_id  {segment_like_id}'s length"
            f" is not in {settings.SEGMENT_ID_PERMIT_LENGTH}")
    cdb_engine = get_cdb_engine(virtual_factory)
    with cdb_engine.connect() as c:
        sql = text(f"""
        SELECT AVG_DATA, CMF_20  FROM MESMGR.CSAMSPCDAT A
          WHERE A.CHAR_ID = '{char_id}'
          AND A.SEGMENT_LOT_ID = '{segment_like_id}'
          order by CMF_20 desc
        """)
        data = c.execute(sql).fetchone()
        if data is None:
            return None
        else:
            return data._mapping


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.SPC_DATA_CACHE_TIME), info=settings.DEBUG)
def get_unit_latest_spc_data_by_operation_id_tuple(unit_id, operation_id_tuple: Tuple[str],
                                                   virtual_factory: common.VirtualFactory) -> pd.DataFrame:
    sql = text(f"""
        SELECT usr_cmf_07, ext_mv, spec_id, sys_time, tran_time from spcmgr.tqs_summary_data
        where 1 = 1
        and usr_cmf_07 = '{unit_id}'
        and ({generate_spec_like_query('spec_id', operation_id_tuple)})
        order by sys_time desc
    """)

    with get_cdb_engine(virtual_factory).connect() as c:
        df = pd.read_sql(sql, c)
        df = df.drop_duplicates(subset=['spec_id'], keep='first')
        return df


def get_mat_info(mat_id: str) -> Dict:
    with get_cdb_engine(common.VirtualFactory.L2W).connect() as c:
        df = pd.read_sql(text(f"select * from MESMGR.MWIPMATDEF where MAT_ID = '{mat_id}'"), c)

    if len(df) == 0:
        with get_cdb_engine(common.VirtualFactory.L1W).connect() as c:
            df = pd.read_sql(text(f"select * from MESMGR.MWIPMATDEF where MAT_ID = '{mat_id}'"), c)

    assert len(df) == 1, rf"mat_id {mat_id} is not unique or not none"

    return df.iloc[0, :].to_dict()


# ---------------------------------mat & spec -------------------------
@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.SPEC_DATA_CACHE_TIME), info=settings.DEBUG)
def get_wafering_spec_by_material_and_operation(mat_id: str, operation_id_tuple: Tuple[str],
                                                virtual_factory: common.VirtualFactory) -> pd.DataFrame:
    cdb_engine = get_cdb_engine(virtual_factory)
    if virtual_factory == common.VirtualFactory.L1W:
        factory = 'WE1'
    else:
        factory = 'L2W'
    sql = text(f"""
WITH MAT_LIST AS
 (SELECT A.MAT_CMF_1, A.MAT_ID, A.MAT_VER, B.FLOW, C.OPER
    FROM MESMGR.MWIPMATDEF A, MESMGR.MWIPMATFLW B, MESMGR.MWIPFLWOPR C
   WHERE A.FACTORY = '{factory}'
     AND A.MAT_ID = '{mat_id}'
     AND C.OPER IN {operation_id_tuple}
--      AND A.DEACTIVE_FLAG <> 'Y'
     AND A.DELETE_FLAG <> 'Y'
     AND A.MAT_ID = B.MAT_ID(+)
     AND A.MAT_VER = B.MAT_VER(+)
     AND B.FLOW = C.FLOW(+)
     AND FIRST_FLOW <> ' '
     AND A.FIRST_FLOW = B.FLOW(+)
   ORDER BY A.MAT_ID, A.MAT_VER, B.FLOW_SEQ_NUM, C.SEQ_NUM
  ),
MAT_SPM AS
 (SELECT A.MAT_CMF_1, B.MAT_ID, B.MAT_VER, B.FLOW, B.OPER, B.SPEC_REL_ID
    FROM MAT_LIST A, MESMGR.MSPMRELDEF B
   WHERE A.MAT_ID = B.MAT_ID(+)
     AND A.MAT_VER = B.MAT_VER(+)
     AND A.FLOW = B.FLOW(+)
     AND A.OPER = B.OPER(+)),
SPM_VER AS
 (SELECT C.MAT_CMF_1,
         C.MAT_ID,
         C.MAT_VER,
         C.FLOW,
         C.OPER,
         C.SPEC_REL_ID,
         MAX(D.SPEC_REL_VER) AS SPEC_REL_VER
    FROM MAT_SPM C,
         (SELECT *
            FROM MESMGR.MSPMRELVER
           WHERE APPROVAL_FLAG = 'Y'
             AND RELEASE_FLAG = 'Y') D
   WHERE 1 = 1
     AND C.SPEC_REL_ID = D.SPEC_REL_ID(+)
   GROUP BY C.MAT_CMF_1, C.MAT_ID, C.MAT_VER, C.FLOW, C.OPER, C.SPEC_REL_ID),
CHAR_LIST AS
 (SELECT E.MAT_CMF_1,
         E.MAT_ID,
         E.MAT_VER,
         E.FLOW,
         E.OPER,
         E.SPEC_REL_ID,
         E.SPEC_REL_VER,
         F.CHAR_ID,
         F.LOWER_SPEC_LIMIT,
         F.TARGET_VALUE,
         F.UPPER_SPEC_LIMIT
    FROM SPM_VER E
    LEFT JOIN MESMGR.MSPMRELCHR F
      ON E.SPEC_REL_ID = F.SPEC_REL_ID
     AND E.SPEC_REL_VER = F.SPEC_REL_VER),
CHAR_ATTR AS
 (SELECT *
    FROM (SELECT A.*,
                 B.ATTR_NAME,
                 DECODE(ATTR_VALUE, '[Null]', ' ', ATTR_VALUE) AS ATTR_VALUE
            FROM CHAR_LIST A,
                 (SELECT *
                    FROM MESMGR.MSPMATRSTS
                   WHERE ATTR_NAME IN ('QA_AUDIT_FLAG', 'IE2_AUDIT_FLAG')) B
           WHERE 1 = 1
             AND A.SPEC_REL_ID = B.SPEC_REL_ID(+)
             AND A.SPEC_REL_VER = B.SPEC_REL_VER(+)
             AND A.CHAR_ID = B.CHAR_ID(+))
  PIVOT(MAX(ATTR_VALUE)
     FOR ATTR_NAME IN('QA_AUDIT_FLAG' "QA_AUDIT_FLAG",
                     'IE2_AUDIT_FLAG' "IE2_AUDIT_FLAG"))
   ORDER BY MAT_ID, MAT_VER, FLOW, OPER)
SELECT * FROM CHAR_ATTR WHERE 1 = 1
AND CHAR_ID is not null 
    """)
    with cdb_engine.connect() as c:
        df = pd.read_sql(sql, c)
        df['lower_spec_limit'] = df.apply(lambda x: mes_db_utils.change_limit_to_float(x['lower_spec_limit'],
                                                                                       'lower'), axis=1)
        df['upper_spec_limit'] = df.apply(lambda x: mes_db_utils.change_limit_to_float(x['upper_spec_limit'],
                                                                                       'upper'), axis=1)
        df['ie2_audit_flag'] = df.apply(
            lambda x: mes_db_utils.change_str_to_boolean(x['ie2_audit_flag']), axis=1)
        df['qa_audit_flag'] = df.apply(
            lambda x: mes_db_utils.change_str_to_boolean(x['qa_audit_flag']), axis=1)

        return df


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.SPEC_DATA_CACHE_TIME), info=settings.DEBUG)
def get_spec_id_list_by_oper_id(oper_id, virtual_factory: common.VirtualFactory):
    sql = text(f"""
    select distinct (a.char_id) from mesmgr.MSPMRELCHR a join mesmgr.MSPMRELDEF b
    on a.SPEC_REL_ID = b.SPEC_REL_ID
    where 1 = 1
    and oper = '{oper_id}'
    """)
    if virtual_factory != common.VirtualFactory.ALL:
        with get_cdb_engine(virtual_factory).connect() as c:
            data_list = c.execute(sql).fetchall()
            return {d[0] for d in data_list}
    else:
        l1w_set = get_spec_id_list_by_oper_id(oper_id, common.VirtualFactory.L1W)
        l2w_set = get_spec_id_list_by_oper_id(oper_id, common.VirtualFactory.L2W)
        return l1w_set | l2w_set


@cached(cache=TTLCache(maxsize=settings.MES_QUERY_CACHE_SIZE, ttl=settings.SPEC_DATA_CACHE_TIME), info=settings.DEBUG)
def get_tp_key_info():
    sql = text(f"""
    SELECT key_1, key_2, key_3 FROM MESMGR.MGCMTBLDAT T
    WHERE 1 = 1
    AND T.TABLE_NAME = 'TP_TYPE'
    """)
    with get_cdb_engine(common.VirtualFactory.L1W).connect() as c:
        data_list_l1w = c.execute(sql).fetchall()

    with get_cdb_engine(common.VirtualFactory.L2W).connect() as c:
        data_list_l2w = c.execute(sql).fetchall()

    key1_set = {d[0] for d in data_list_l1w} | {d[0] for d in data_list_l2w}
    key2_set = {d[1] for d in data_list_l1w} | {d[1] for d in data_list_l2w}
    key3_set = {d[2] for d in data_list_l1w} | {d[2] for d in data_list_l2w}
    return {
        'key_1': key1_set,
        'key_2': key2_set,
        'key_3': key3_set,
    }
