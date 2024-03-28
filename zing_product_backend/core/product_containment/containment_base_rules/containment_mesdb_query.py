import typing
import pandas as pd

from zing_product_backend.app_db.mes_db_query import get_cdb_engine, get_lot_sts, get_sublot_sts, \
    get_spec_info, get_csamspcdat_data, get_tqs_summary_data

if typing.TYPE_CHECKING:
    from zing_product_backend.core.product_containment.parser_core.containment_structure import Product, LotLikeProduct, \
        SublotProduct

CSAMSPCDAT_SAMPLE_TYPE_MAPPING = {
    'LOT': 'WAFFER',
    'INGOT': 'INGOT',
    'SEGMENT': 'SEGMENT',
    'IE2': 'SEGMENT',
    'IE3': 'SEGMENT',
}


def get_material_from_product(target_product: 'Product') -> str:
    target_product_v_factory = target_product.virtual_factory
    if isinstance(target_product, LotLikeProduct):
        lot_sts = get_lot_sts(target_product_v_factory, target_product.id)
        mat_id = lot_sts['mat_id']
    elif isinstance(target_product, SublotProduct):
        sublot_sts = get_sublot_sts(target_product_v_factory, target_product.id)
        mat_id = sublot_sts['mat_id']

    else:
        raise ValueError(f'Unknown product type: {target_product}')

    return mat_id


def get_spec_value_df(spec_id_df: pd.DataFrame, target_product: 'SublotProduct') -> pd.DataFrame:
    assert 'spec_id' in spec_id_df.columns
    available_sample_type = ['WAFER', 'LOT', 'RASOURCE', 'IE3', 'INGOT', 'IE2', 'SEGMENT']
    final_data_df_list = []
    spec_id_df['oper'] = spec_id_df['spec_id'].str[:4]
    for oper_id, oper_df in spec_id_df.groupby('oper'):
        if len(oper_df) <= 2:
            # query by spec individually
            for spec_id in oper_df['spec_id']:
                sample_type = get_spec_info(spec_id, target_product.virtual_factory)['sample_type']
                assert sample_type in available_sample_type
                if sample_type in ['WAFER', 'RESOURCE']:
                    data_df = get_tqs_summary_data(target_product.id, spec_id=spec_id, oper_id=None,
                                                   virtual_factory=target_product.virtual_factory)
                else:
                    csamspcdat_sample_type = CSAMSPCDAT_SAMPLE_TYPE_MAPPING[sample_type]
                    data_df = get_csamspcdat_data(target_product.id, sample_type, spec_id=spec_id, oper_id=oper_id,
                                                  sample_type=csamspcdat_sample_type,
                                                  virtual_factory=target_product.virtual_factory)
                final_data_df_list.append(data_df)

        else:
            sample_type_set = set()
            for spec_id in oper_df['spec_id']:
                spec_info = get_spec_info(spec_id, target_product.virtual_factory)
                sample_type_set.add(spec_info['sample_type'])

            if 'WAFER' in sample_type_set or 'RESOURCE' in sample_type_set:
                df = get_tqs_summary_data(target_product.id, spec_id=None, oper_id=oper_id,
                                          virtual_factory=target_product.virtual_factory)
                final_data_df_list.append(df)

            for sample_type in sample_type_set:
                csamspcdat_sample_type = CSAMSPCDAT_SAMPLE_TYPE_MAPPING.get(sample_type, None)

                if sample_type == 'INGOT':
                    sample_id = target_product.get_sts_data('sublot_cmf_1')

                elif sample_type == 'IE2':
                    group_id = target_product.get_sts_data('sublot_cmf_16')
                    if group_id == ' ':
                        group_id = target_product.id[:6] + '00'
                    sample_id = group_id

                elif sample_type == 'IE3':
                    sample_id = target_product.get_sts_data('sublot_cmf_17')

                elif sample_type == 'SEGMENT':
                    sample_id = target_product.get_sts_data('sublot_cmf_2')

                elif sample_type == 'LOT':
                    sample_id = target_product.id  # use wafer_id for lot sample data
                else:
                    sample_id = None

                if sample_id:
                    df = get_csamspcdat_data(sample_id, csamspcdat_sample_type, spec_id=None,
                                             oper_id=oper_id,
                                             virtual_factory=target_product.virtual_factory)
                    final_data_df_list.append(df)

    final_data_df = pd.concat(final_data_df_list)
    return spec_id_df.merge(final_data_df, on='spec_id')
