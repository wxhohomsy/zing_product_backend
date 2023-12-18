from typing import Any, List, Optional, Literal
from pydantic import BaseModel, Field, model_validator
from zing_product_backend.core.product_containment.containment_constants import *


class BaseRuleBase(BaseModel):
    field: Optional[str] = None
    value_type: Optional[BaseRuleParaType] = None
    value_source: Optional[t_value_source] = None
    value: Optional[Union[List, str, int, float]] = None
    operator: Optional[BaseRuleOperator] = None
    rules: Optional[List['BaseRuleBase']] = None
    rules_group_name: Optional[str] = None
    combinator: Optional[Literal['and', 'or']] = None
    not_flag: bool = Field(default=False, alias='not')

    @model_validator(mode='before')
    @classmethod
    def check_rules_set_none(cls, data_dict: dict) -> dict:
        if 'rules' not in data_dict or data_dict['rules'] is None:
            assert data_dict.get('field_name') is not None, "field_name must be set if rules is None"
            assert data_dict.get('value_type') is not None, "value_type must be set if rules is None"
            assert data_dict.get('value') is not None, "value must be set if rules is None"
        else:
            assert data_dict.get('field_name') is None, "field_name must be None if rules is not None"
            assert data_dict.get('value_type') is None, "value_type must be None if rules is not None"
            assert data_dict.get('value') is None, "value must be None if rules is not None"
        return data_dict


# ------------ spc ooc oos rule -------------
class CharRule(BaseModel):
    char_id: str
    exclude: bool = Field(default=False)


class OperationRule(BaseModel):
    operation_id: str


class SpcBaseRule(BaseModel):
    rule_name: Literal['spc_ooc', 'spc_oos']
    char_rules: List[CharRule]
    operation_rules: List[OperationRule]
    ie2_audit_flag_enable: bool = True
    qa_audit_flag_enable: bool = True


# --------------------- growing fdc rule ------------------------------------
class FdcBaseRule(BaseRuleBase):
    rule_name: FdcBaseRuleName
    rules:  Optional[List['FdcBaseRule']]





