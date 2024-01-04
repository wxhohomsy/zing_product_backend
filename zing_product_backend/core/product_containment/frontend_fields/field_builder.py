from decimal import Decimal
import warnings
from typing import List, Union, Tuple, Type
from sqlalchemy import text, inspect, Table
from sqlalchemy.orm import DeclarativeBase
from zing_product_backend.core.product_containment.containment_constants import *
from .front_end_field_cnstants import *
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


def build_spc_oos_ooc_fields():
    # fields [oper, char_id, 'OOS', 'NOTOOS]
    pass


def build_fields_from_custom_rule():
    pass