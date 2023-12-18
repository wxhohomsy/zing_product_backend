from pydantic import BaseModel
from zing_product_backend.core.product_containment.containment_constants import *


class BaseRuleParas(BaseModel):
    name = 'BaseRuleParas'
    para_type = BaseRuleParaType


class BaseRule(BaseModel):
    RULE_NAME: BaseRuleName


