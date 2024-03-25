from typing import Union
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
            # 'mat_cmf_1', 'mat_id', 'mat_ver', 'flow', 'oper', 'spec_rel_id',
            # 'spec_rel_ver', 'char_id', 'lower_spec_limit', 'target_value',
            # 'upper_spec_limit', 'qa_audit_flag', 'ie2_audit_flag'
        else:
            spec_df = 123

        spec_list = [SpcSpecialSpec.ALL_SPEC]

    elif SpcSpecialSpec.ANY_SPEC in spec_list:
        spec_list = [SpcSpecialSpec.ANY_SPEC]

    if len(spec_list) == 1 and spec_list[0] == SpcSpecialSpec.ALL_SPEC:
        spec_df = mes_db_query.get_spec_by_material_and_operation(target_product_mat_id)


