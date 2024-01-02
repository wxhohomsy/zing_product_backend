from typing import List, Union, Dict, Set, Literal
from pydantic import BaseModel
from enum import Enum
from .front_end_field_cnstants import *

type_value_source = Literal['value', 'field']


class RuleOperator(BaseModel):
    name: str
    label: str
    arity: int


class Values(BaseModel):
    name: str
    label: str


class Field(BaseModel):
    name: str
    label: str
    placeholder: Union[str, None] = None
    operators: Union[list[RuleOperator], None] = None
    valueSources: Union[list[type_value_source], None] = None
    values: Union[List[Values], None] = None
    valueEditorType: Union[ValueEditor, None] = None
    inputType: Union[InputType, None] = None
    defaultValue: Union[str, None] = None
