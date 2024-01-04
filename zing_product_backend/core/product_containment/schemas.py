from typing import Any, List, Optional, Literal
from pydantic import BaseModel, Field, model_validator
from zing_product_backend.core.product_containment.containment_constants import *
from zing_product_backend.core import common


class BaseRuleBase(BaseModel):
    field: Optional[str] = None
    value: Optional[Any] = None
    operator: Optional[RuleOperator] = None


class BaseRule(BaseRuleBase):
    base_rules: List[BaseRuleBase]
    rule_name: str
    rule_class: ContainmentBaseRuleClass


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






