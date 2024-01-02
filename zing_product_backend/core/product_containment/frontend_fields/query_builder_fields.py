import warnings
from typing import List, Union, Tuple, Type
from decimal import Decimal
from sqlalchemy import text, inspect, Table
from sqlalchemy.orm import DeclarativeBase
from . import fields_schema
from .front_end_field_cnstants import *
from zing_product_backend.core import common


def generate_fields_main(containment_base_rule: common.ContainmentBaseRuleClass):
    if containment_base_rule in containment_base_rule.MWIPLOTSTS:


def build_fields_from_sql_table(db_table: Union[Table, Type[DeclarativeBase]]) -> List[fields_schema.Field]:
    to_return_field_list: List[fields_schema.Field] = []
    for col in inspect(db_table).columns:
        input_type: InputType = None
        value_editor_type: ValueEditor = ValueEditor.TEXT
        if isinstance(col.type.python_type, (Decimal, float, int)):
            input_type = InputType.NUMBER
        elif isinstance(col.type.python_type, str):
            input_type = InputType.TEXT
        elif isinstance(col.type.python_type, bool):
            input_type = InputType.CHECKBOX
            value_editor_type = ValueEditor.CHECKBOX
        else:
            warnings.warn(f'Unknown type {col.type} for column {col.name}')

        to_return_field_list.append(fields_schema.Field(
            name=col.name,
            label=col.name,
            inputType=input_type,
            valueEditorType=value_editor_type,
        ))
