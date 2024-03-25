import datetime
from uuid import UUID
from typing import List, Dict, Set, Literal, Union
from pydantic import BaseModel
from zing_product_backend.core import common, common_type
from zing_product_backend.services.containment_rules import schemas as containment_rule_schemas


class TPWaferInfo(BaseModel):
    id: int
    last_updated_time: datetime.datetime
    tp_id: str
    oper: Union[str, None]
    picked: bool
    pick_time: Union[datetime.datetime, None]
    from_lot_id: str
    key_1: str
    key_2: str
    key_3: str


class TpAssignLotInfo(BaseModel):
    last_tran_time: datetime.datetime
    oper_in_time: datetime.datetime
    last_updated_time: datetime.datetime
    lot_id: str
    mat_id: str
    flow: str
    oper: str
    tp_list: list[TPWaferInfo]
    to_sample_tp_count: int


class TpSamplePlanOptions(BaseModel):
    key_1: Set[str]
    key_2: Set[str]
    key_3: Set[str]
    sample_type: Set[common.TpSampleType]
    frequency_type: Set[common.TpFrequencyType]
    containment_rules: List[containment_rule_schemas.ContainmentRuleInfo]


class TpSamplePlanInfo(BaseModel):
    id: int
    sample_plan_name: str
    key_1: str
    key_2: str
    key_3: str
    sample_type: common.TpSampleType
    frequency_type: Union[common.TpFrequencyType, None]
    frequency_value: Union[int, None]
    must_include_seed_tail: bool
    plan_priority: int
    containment_rule_id: int
    containment_rule_name: str
    consider_unslicing_block: bool
    consider_unreached_block: bool
    updated_time: datetime.datetime
    updated_by: UUID
    updated_user_name: str


class InsertTpSamplePlan(BaseModel):
    sample_plan_name: str
    key_1: str
    key_2: str
    key_3: str
    sample_type: common.TpSampleType
    frequency_type: Union[common.TpFrequencyType, None]
    frequency_value: Union[int, None]
    consider_unslicing_block: bool
    consider_unreached_block: bool
    must_include_seed_tail: bool
    plan_priority: int
    containment_rule_id: int


class UpdateTpSampleRuleInfo(BaseModel):
    id: int
    sample_plan_name: str
    key_1: str
    key_2: str
    key_3: str
    sample_type: common.TpSampleType
    frequency_type: Union[common.TpFrequencyType, None]
    frequency_value: Union[int, None]
    consider_unslicing_block: bool
    consider_unreached_block: bool
    must_include_seed_tail: bool
    plan_priority: int
    containment_rule_id: int


class DeleteTpSampleRule(BaseModel):
    id: int
