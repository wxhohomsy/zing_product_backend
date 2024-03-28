from typing import Union

import pandas as pd

import zing_product_backend.core.product_containment.crud
from zing_product_backend.app_db import mes_db_query
from zing_product_backend.core.product_containment.containment_constants import (ContainmentBaseRuleClass,
                                                                                 SpcSpecialSpec, SpcOosOperators,
                                                                                 SpcValueOperators,
                                                                                 ContainmentBaseRuleClass)
from zing_product_backend.core.product_containment.parser_core.containment_structure import \
    Product, WaferingSegment, Sublot, Lot, GrowingSegment
from zing_product_backend.core.product_containment.parser_core.result_structure import (
    ContainmentResult, ContainmentStatus, ContainmentDetailData
)
from .. import local_db_query


def parse_spec(operator: SpcOosOperators, field_list: list[str],
               target_product: Union['Sublot', 'WaferingSegment', 'GrowingSegment'],
               rule_class: 'ContainmentBaseRuleClass') -> ContainmentResult:

    assert len(field_list) > 1, 'field_list must have at least 2 fields'
    target_product_mat_id = target_product.get_sts_data('mat_id')
    oper_id = field_list[0]
    spec_list = field_list[1:]
    if SpcSpecialSpec.ALL_SPEC in spec_list:
        all_pass = True
        if rule_class == ContainmentBaseRuleClass.SPC_OOS:
            spec_df = mes_db_query.get_spec_by_material_and_operation(target_product_mat_id)
            # only consider row with either qa_audit_flag or ie2_audit_flag == True
            spec_df = spec_df[(spec_df['qa_audit_flag'] == True) | (spec_df['ie2_audit_flag'] == True)]
            # 'mat_cmf_1', 'mat_id', 'mat_ver', 'flow', 'oper', 'spec_rel_id',
            # 'spec_rel_ver', 'char_id', 'lower_spec_limit', 'target_value',
            # 'upper_spec_limit', 'qa_audit_flag', 'ie2_audit_flag'
        else:
            spec_df = get_ooc_spec(target_product)
            # only column char_id, lower_spec_limit, upper_spec_limit is guaranteed in both df

        spec_list = [SpcSpecialSpec.ALL_SPEC]

    elif SpcSpecialSpec.ANY_SPEC in spec_list:
        spec_list = [SpcSpecialSpec.ANY_SPEC]

    if len(spec_list) == 1 and spec_list[0] == SpcSpecialSpec.ALL_SPEC:
        spec_df = mes_db_query.get_spec_by_material_and_operation(target_product_mat_id)


def get_ooc_spec(target_product):
    # laze import
    from ...containment_rules.containment_rule_main import containment_rule_parse_by_containment_id
    spec_df = zing_product_backend.core.product_containment.crud.get_ooc_spec_with_containment_id()
    # columns: ['id', 'containment_rule_id', 'spec_id', 'lower_limit', 'upper_limit', 'create_time', 'create_user_name',
    #           'updated_time', 'updated_user_name', 'rule_delete_flag']
    filtered_data_series_list = []
    for _, spec_data in spec_df.iterrows():
        containment_id = spec_data['containment_id']
        containment_result = containment_rule_parse_by_containment_id(containment_id, target_product)
        if containment_result.result_status == ContainmentStatus.CATCH:
            filtered_data_series_list.append(spec_data)

    return_df = pd.concat(filtered_data_series_list, axis=0)
    return_df.reset_index(drop=True, inplace=True)
    return_df.rename(columns={'lower_limit': 'lower_spec_limit', 'upper_limit': 'upper_spec_limit',
                              'spec_id': 'char_id'}, inplace=True)
    return return_df


def check_spec(char_id, lower_limit: float|None, upper_limit: float|None) -> bool:
    # do not consider target, may be added later
    pass


