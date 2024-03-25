from typing import TYPE_CHECKING, Callable, Dict, Union
from sqlalchemy import text
from zing_product_backend.core.product_containment.containment_constants import ContainmentBaseRuleClass
from zing_product_backend.core import exceptions
from zing_product_backend.app_db import external_tables
from zing_product_backend.reporting import system_log
from .. import mesdb_query, local_db_query, field_utils
from ...parser_core.result_structure import ContainmentResult, ContainmentStatus, ContainmentDetailData

if TYPE_CHECKING:
    from ...parser_core.containment_structure import ContainmentBaseRule, Product
    from zing_product_backend.core import common


def mat_group_main(base_rule: 'ContainmentBaseRule', target_product: 'Product') -> ContainmentResult:
    assert base_rule.rule_class in [ContainmentBaseRuleClass.MAT_GROUP], rf"Invalid rule class: {base_rule.rule_class}"


def mat_yield_group_main(base_rule: 'ContainmentBaseRule', target_product: 'Product') -> ContainmentResult:
    target_product_mat = mesdb_query.get_material_from_product(target_product)
    target_product_mat_group = local_db_query.get_yield_groups_by_mat_id(target_product_mat)
    field_operator = base_rule.rule_data['operator']
    field_value = base_rule.rule_data['value']
    compared_result = field_utils.compute_numeric_field_result(field_operator, field_value,
                                                               target_product_mat_group)
    result_status = ContainmentStatus.CATCH if compared_result else ContainmentStatus.PASS
    detail_data = ContainmentDetailData(base_rule=base_rule, target_object=target_product,
                                        result_status=result_status, actual_value=target_product_mat_group)
    return ContainmentResult(result_status=result_status, target_object=target_product,
                             detail_data_list=[detail_data])
