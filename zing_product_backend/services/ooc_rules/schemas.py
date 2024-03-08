from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OOCRuleCreate(BaseModel):
    containment_rule_id: int
    spec_id: str
    lower_limit: Optional[float]
    upper_limit: Optional[float]


class OOCRuleUpdate(BaseModel):
    id: int
    lower_limit: Optional[float]
    upper_limit: Optional[float]


class OOCRule(BaseModel):
    id: int
    containment_rule_id: int
    spec_id: str
    lower_limit: Optional[float]
    upper_limit: Optional[float]
    create_time: datetime
    create_user_name: str
    updated_time: datetime
    updated_user_name: str
    rule_delete_flag: bool

    class Config:
        orm_mode = True
