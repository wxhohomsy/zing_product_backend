from pydantic import BaseModel, Json
from typing import List, Union, Dict, Set, Literal
from zing_product_backend.core import common


class ContainmentBaseRuleClassInfo(BaseModel):
    id: int
    class_name: common.ContainmentBaseRuleClass
    class_type: common.ContainmentBaseRuleType


class ContainmentBaseRuleInfo(BaseModel):
    id: int
    affected_rule_group_id_list: List[int]
    rule_class: common.ContainmentBaseRuleClass  # DATA_OOS, DATA_OOC, PULLER_ID, END_TIME, HC_REDUCE_RULE ...
    rule_name: common.ContainmentBaseRuleType  # SQL_TABLE or CUSTOM_FUNCTION
    rule_data: Json
    changeable: bool
    created_by: str
    created_time: str
    updated_by: str
    updated_time: str


class ContainmentRuleGroupInfo(BaseModel):
    id: int
    included_rule_id_list: List[int]
    rule_name: str
    rule_data: Json
    changeable: bool
    created_by: str
    created_time: str
    updated_by: str
    updated_time: str