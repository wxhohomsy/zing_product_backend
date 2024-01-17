from typing import List, Union, Dict, Set, Literal
from uuid import UUID
import datetime
from pydantic import BaseModel
from zing_product_backend.core import common
from zing_product_backend.core.product_containment.containment_constants import *
from zing_product_backend.core.product_containment.frontend_fields import fields_schema


class ContainmentBaseRuleClassInfo(BaseModel):
    is_sql: bool
    is_spc: bool
    fields: List[fields_schema.Field]


class ContainmentBaseRuleInfo(BaseModel):
    id: int
    affected_rule_id_list: List[int]
    rule_name: str
    rule_class: ContainmentBaseRuleClass  # DATA_OOS, DATA_OOC, PULLER_ID, END_TIME, HC_REDUCE_RULE ...
    rule_data: dict
    rule_sql: str
    containment_object_type: ProductObjectType
    changeable: bool
    virtual_factory: common.VirtualFactory
    created_by: UUID
    created_time: datetime.datetime
    updated_by: UUID
    updated_time: datetime.datetime
    created_user_name: str
    updated_user_name: str


class UpdateContainmentBaseRuleInfo(BaseModel):
    id: int
    rule_name: str
    rule_data: dict
    rule_sql: str
    changeable: bool
    containment_object_type: ProductObjectType
    virtual_factory: common.VirtualFactory


class DeleteContainmentBaseRule(BaseModel):
    id: int


class InsertContainmentBaseRule(BaseModel):
    rule_name: str
    rule_class: ContainmentBaseRuleClass
    rule_data: dict
    containment_object_type: ProductObjectType
    rule_sql: str
    virtual_factory: common.VirtualFactory
    changeable: bool = True


class ContainmentRuleInfo(BaseModel):
    id: int
    rule_name: str
    included_base_rule_id_list: List[int]
    rule_data: dict
    changeable: bool
    rule_description: str
    created_by: UUID
    created_time: datetime.datetime
    updated_by: UUID
    updated_time: datetime.datetime
    created_user_name: str
    updated_user_name: str


class DeleteContainmentRule(BaseModel):
    id: int


class InsertContainmentRule(BaseModel):
    rule_name: str
    rule_data: dict
    rule_sql: str
    rule_description: str
    changeable: bool = True


class UpdateContainmentRule(BaseModel):
    id: int
    rule_name: str
    rule_data: dict
    rule_sql: str
    changeable: bool = True
    rule_description: str
