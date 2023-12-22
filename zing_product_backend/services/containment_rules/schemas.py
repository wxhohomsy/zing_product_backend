from pydantic import BaseModel, Json
from typing import List, Union, Dict, Set, Literal
from zing_product_backend.core import common


class ContainmentBaseRuleClassInfo(BaseModel):
    id: int
    class_name: common.ContainmentBaseRuleClass
    class_type: common.ContainmentBaseRuleType

class FieldOperator(BaseModel):
    name : str
    label : str

class QueryField(BaseModel):
    name: str
    label: str
    operators: Union[None|]


# export type AllContainmentBaseRuleInfo = {
#     "success": boolean,
#     "error_message": string,
#     "success_message": string,
#     "data": {
#         "id": number,
#         "affected_rule_group_id_list": number[],  //rule group that will be affected if this rule is changed
#         "rule_class": string,
#         "rule_name": string,
#         "rule_data": string,
#         "changeable": boolean,
#         "created_by": string,
#         "created_time": string,
#         "updated_by": string,
#         "updated_time": string,
#     }[],
#     "detail": string
# }


class ContainmentBaseRuleInfo(BaseModel):
    id: int
    affected_rule_group_id_list: List[int]
    rule_class: common.ContainmentBaseRuleClass
    rule_name: common.ContainmentBaseRuleType
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