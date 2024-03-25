from typing import TYPE_CHECKING
from zing_product_backend.core.product_containment.containment_constants import ContainmentBaseRuleClass, \
    IngotFdcField
from .. import field_utils
from . import fdc_data_fetch
from ...parser_core.result_structure import ContainmentResult, ContainmentStatus, ContainmentDetailData
from ...parser_core.containment_structure import ContainmentBaseRule, Product, Sublot
from zing_product_backend.core import common


def m1_fdc_main(base_rule: 'ContainmentBaseRule', target_product: 'Product') -> ContainmentResult:
    assert isinstance(target_product, Sublot), 'm1_fdc_main only accept sublot'
    wafer_position = float(target_product.get_sts_data('sublot_cmf_9')) * 10  #unit in mm
    wafer_position_index = int(wafer_position)
    field = IngotFdcField(base_rule.rule_data['field'])
    ingot_data_array = fdc_data_fetch.get_ingot_fdc_data(base_rule, field)
    field_operator = base_rule.rule_data['operator']
    field_value = field_utils.change_field_value_to_float(base_rule.rule_data['value'])
    actual_value = ingot_data_array[wafer_position_index]
    compared_result = field_utils.compute_numeric_field_result(field_operator, field_value,
                                                               actual_value)

    result_status = ContainmentStatus.CATCH if compared_result else ContainmentStatus.PASS

    detail_data = ContainmentDetailData(base_rule=base_rule, target_object=target_product,
                                        result_status=result_status, actual_value=actual_value)

    return ContainmentResult(result_status=result_status, target_object=target_product,
                             detail_data_list=[detail_data])




