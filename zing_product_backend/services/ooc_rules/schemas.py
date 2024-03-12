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

# class OOCRules(Base):
#     __tablename__ = 'ooc_rules'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     containment_rule_id = Column(Integer, ForeignKey(ContainmentRule.id), nullable=False, index=True)
#     spec_id: Mapped[str] = Column(VARCHAR(), nullable=False, index=True)
#     lower_limit = Column(Float)
#     upper_limit = Column(Float)
#     create_time: Mapped[datetime.datetime] = Column(DateTime, default=func.now(), nullable=False)
#     create_user_name = Column(VARCHAR(), ForeignKey(auth_model.User.user_name), nullable=False)
#     updated_time = Column(DateTime(), nullable=False, default=func.now(), onupdate=func.now())
#     updated_user_name = Column(VARCHAR(), ForeignKey(auth_model.User.user_name), nullable=False)
#     rule_delete_flag: Mapped[str] = Column(Boolean(), default=False)


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

