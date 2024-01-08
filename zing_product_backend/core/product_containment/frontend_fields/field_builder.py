from decimal import Decimal
import warnings
from typing import List, Union, Tuple, Type
from sqlalchemy import text, inspect, Table
from sqlalchemy.orm import DeclarativeBase
from zing_product_backend.app_db import mes_db_query
from zing_product_backend.core.product_containment.containment_constants import *
from . import fields_schema
from zing_product_backend.core import common


def build_fields_from_sql_rule(db_table: Union[Table, Type[DeclarativeBase]]) -> List[fields_schema.Field]:
    to_return_field_list: List[fields_schema.Field] = []
    for col in inspect(db_table).columns:
        input_type: RuleInputType = None
        value_editor_type: RuleValueEditor = RuleValueEditor.TEXT
        if issubclass(col.type.python_type, (Decimal, float, int)):
            input_type = RuleInputType.NUMBER
        elif issubclass(col.type.python_type, str):
            input_type = RuleInputType.TEXT
        elif issubclass(col.type.python_type, bool):
            input_type = RuleInputType.CHECKBOX
            value_editor_type = RuleValueEditor.CHECKBOX
        else:
            warnings.warn(f'Unknown type {col.type} for column {col.name}')
            print(col.type.python_type)

        to_return_field_list.append(fields_schema.Field(
            name=col.name,
            inputType=input_type,
            valueEditorType=value_editor_type,
        ))

    return to_return_field_list


def build_spc_fields(base_rule_class: ContainmentBaseRuleClass, virtual_factory: common.VirtualFactory):
    operator_list = []
    if base_rule_class in [ContainmentBaseRuleClass.SPC_OOC, ContainmentBaseRuleClass.SPC_OOS]:
        for operator_name in SpcOosOperators:
            operator_list.append(fields_schema.RuleOperator(name=operator_name, label=operator_name, arity=0))

    elif base_rule_class == ContainmentBaseRuleClass.SPC_VALUE:
        for operator in SPC_VALUE_OPERATOR_NAMES:
            operator_list.append(
                fields_schema.RuleOperator(name=operator, label=operator, arity=1)
            )

    field_list: List[fields_schema.Field] = []
    oper_list = mes_db_query.get_available_oper_id_list('2100', '6898', virtual_factory)

    for oper_id in oper_list:
        field_list.append(fields_schema.Field(
            name=oper_id,
            label=oper_id,
            inputType=RuleInputType.CHECKBOX,
            valueEditorType=RuleValueEditor.CHECKBOX,
            operators=[
                fields_schema.RuleOperator(name='OK', label='OK', arity=0),
                fields_schema.RuleOperator(name='NG', label='NG', arity=0),
                fields_schema.RuleOperator(name='No', label='ERROR', arity=0),
                       ],
        ))
    return field_list


def build_fields_from_custom_rule(base_rule_class: ContainmentBaseRuleClass, virtual_factory: common.VirtualFactory):
    if base_rule_class in [ContainmentBaseRuleClass.SPC_OOC, ContainmentBaseRuleClass.SPC_OOS,
                           ContainmentBaseRuleClass.SPC_VALUE]:
        return build_spc_fields(base_rule_class, virtual_factory)
    else:
        warnings.warn(f'Unknown rule class {base_rule_class}')
        return []

