import datetime
import uuid
from typing import Optional, Set, Literal, List, Union
from fastapi_users import schemas, models
from pydantic import BaseModel, ConfigDict
from zing_product_backend.core import common


class User(models.UserProtocol):
    user_name: str


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class PrivilegeGroupInfo(BaseModel):
    group_name: str
    group_description: Union[str, None]
    id: int


class PrivilegeRuleInfo(BaseModel):
    rule_name: str
    rule_description: Union[str, None]
    id: int


class UserInfo(BaseModel):
    user_name: str
    email: str
    is_active: bool
    id: uuid.UUID
    privilege_groups: List[PrivilegeGroupInfo]
    privilege_rules: List[PrivilegeRuleInfo]


class UserInfoUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class UserCreate(schemas.BaseUserCreate):
    user_name: str


class PrivilegeGroup(BaseModel):
    id: int
    group_name: str
    group_description: Union[str, None]
    created_by: uuid.UUID
    created_time: datetime.datetime
    group_deleted: bool


class PrivilegeGroupWithRules(BaseModel):
    id: int
    group_name: str
    group_description: Union[str, None]
    created_by: uuid.UUID
    created_time: datetime.datetime
    group_deleted: bool
    privilege_rules: List[PrivilegeRuleInfo]


class PrivilegeRuleWithGroups(BaseModel):
    id: int
    rule_name: str
    rule_description: Union[str, None]
    rule_active: bool
    privilege_groups: List[PrivilegeGroupInfo]


class PrivilegeGroupCreate(BaseModel):
    group_name: str
    group_description: Union[str, None]


class PrivilegeRule(BaseModel):
    id: int
    rule_name: common.RuleName
    rule_description: Union[str, None]
    rule_active: bool


class PrivilegeGroupAssign(BaseModel):
    user_id: uuid.UUID
    group_id_list: List[int]


class PrivilegeRuleUpdate(BaseModel):
    id: int
    rule_name: str
    rule_description: Union[str, None]
    rule_active: bool


class PrivilegeRuleCreate(BaseModel):
    group_name: str
    group_description: Union[str, None]


class PrivilegeRuleAssign(BaseModel):
    group_id: int
    rule_id_list: List[int]


# class User(UserBase):
#     privilege_groups: List[PrivilegeGroupBase]
#
#
# class PrivilegeGroup(PrivilegeGroupBase):
#     privilege_rules:  List[PrivilegeRuleBase]
#     users: List[UserBase]
#
#
# class PrivilegeRule(PrivilegeRuleBase):
#     privilege_groups: List[PrivilegeGroupBase]


class UserUpdate(schemas.BaseUserUpdate):
    pass
