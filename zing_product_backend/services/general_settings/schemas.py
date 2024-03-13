import datetime
import uuid
from typing import Union, List, Set, Dict
from pydantic import BaseModel
from zing_product_backend.core import common
from typing import Optional


class MatInfoByGroupType(BaseModel):
    id: int
    mat_id: str
    mat_description: str
    group_name: Union[str, None]
    group_id: Union[int, None]
    group_type: Union[common.MatGroupType, None]
    mat_base_type: common.MatBaseType
    mat_type: str
    mat_grp_1: str
    mat_grp_2: str
    mat_grp_3: str
    mat_grp_4: str
    mat_grp_5: str
    mat_grp_6: str
    mat_grp_7: str
    mat_grp_8: str
    first_flow: str
    created_time: datetime.datetime
    updated_time: datetime.datetime
    updated_by: str


class UpdateMatInfoByGroupTypeBase(BaseModel):
    id: int
    group_id: Union[int, None]


class UpdateMatInfoByGroupType(BaseModel):
    data: List[UpdateMatInfoByGroupTypeBase]


class MatGroupInfo(BaseModel):
    id: int
    group_name: str
    group_type: common.MatGroupType
    description: Union[str, None]
    updated_time: datetime.datetime
    updated_by: str


class MatGroupDetail(MatGroupInfo):
    mat_info_list: List[MatInfoByGroupType]


class CreateMatGroup(BaseModel):
    group_name: str
    description: str


class UpdateMatGroup(BaseModel):
    group_id: int
    group_name: Union[str, None]
    description: Union[str, None]


class DeleteMatGroup(BaseModel):
    group_id: int


class OOCRuleCreate(BaseModel):
    containment_rule_id: int
    spec_id: str
    lower_limit: Union[float, None]
    upper_limit: Union[float, None]


class OOCRuleUpdate(BaseModel):
    id: int
    lower_limit: Union[float, None]
    upper_limit: Union[float, None]


class OOCRules(BaseModel):
    id: int
    containment_rule_id: int
    spec_id: str
    lower_limit: Union[float, None]
    upper_limit: Union[float, None]
    create_time: datetime.datetime
    create_user_name: str
    updated_time: datetime.datetime
    updated_user_name: str
    rule_delete_flag: bool

    class Config:
        from_attributes = True