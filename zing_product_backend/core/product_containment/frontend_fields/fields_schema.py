from typing import List, Union, Dict, Set, Literal
from pydantic import BaseModel
from enum import Enum
from ..containment_constants import *

type_value_source = Literal['value', 'field']


class RuleOperator(BaseModel):
    name: str
    label: str
    arity: int


class RuleValues(BaseModel):
    name: str
    label: str


class Field(BaseModel):
    name: Union[str, List[str]]
    label: Union[str, List[str]] = None
    placeholder: Union[str, None] = None
    operators: Union[list[RuleOperator], None] = None
    valueSources: Union[list[type_value_source], None] = None
    values: Union[List[RuleValues], None] = None
    valueEditorType: Union[RuleValueEditor, None] = None
    inputType: Union[RuleInputType, None] = None
    defaultValue: Union[str, None] = None
