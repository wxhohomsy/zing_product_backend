import warnings
from decimal import Decimal
from sqlalchemy import text, inspect, Table
from sqlalchemy.orm import DeclarativeBase
from . import fields_schema
from zing_product_backend.core.product_containment.frontend_fields import field_builder
from zing_product_backend.core.product_containment.containment_constants import *


def generate_fields_main(containment_base_rule_class: ContainmentBaseRuleClass):
    if RULE_IS_SQL_DICT[containment_base_rule_class]:
        sql_table = RULE_SQL_TABLE_MAPPING[containment_base_rule_class]
        return field_builder.build_fields_from_sql_rule(sql_table)
    else:
        if containment_base_rule_class in [containment_base_rule_class.SPC_OOC, containment_base_rule_class.SPC_OOS]:
            pass
