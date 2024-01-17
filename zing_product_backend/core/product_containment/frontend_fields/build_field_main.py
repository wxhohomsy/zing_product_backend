from . import fields_schema
from zing_product_backend.core.common import VirtualFactory
from zing_product_backend.core.product_containment.frontend_fields import field_builder
from zing_product_backend.core.product_containment.containment_constants import *


async def generate_base_rule_fields_main(
        containment_base_rule_class: ContainmentBaseRuleClass, virtual_factory: VirtualFactory
) -> List[fields_schema.Field]:
    if RULE_IS_SQL_DICT[containment_base_rule_class]:
        sql_table = RULE_SQL_TABLE_MAPPING[containment_base_rule_class]
        return await field_builder.build_fields_from_sql_rule(sql_table) # assume l1w table is same as l2w table
    else:
        return await field_builder.build_fields_from_custom_rule(containment_base_rule_class, virtual_factory)


async def generate_rule_fields_main(containment_rule_name_list: List[str]) -> List[fields_schema.Field]:
    to_return_list = []
    operators = []
    for operator_name in ContainmentStatus:
        operators.append(fields_schema.RuleOperator(name=operator_name, label=operator_name, arity=0))

    for containment_rule_name in containment_rule_name_list:
        to_return_list.append(
            fields_schema.Field(
                name=containment_rule_name,
                label=containment_rule_name,
                inputType=RuleInputType.HIDDEN,
                operators=operators,
            )
        )
    return to_return_list
