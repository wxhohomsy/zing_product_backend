from pydantic import BaseModel
from zing_product_backend.core.product_containment.containment_constants import *


class BaseRuleParas(BaseModel):
    pass


class BaseRule(BaseModel):
    RULE_NAME: BaseRuleName


