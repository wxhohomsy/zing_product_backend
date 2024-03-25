import datetime
from typing import List, Dict, Set, Literal, Union
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr, relationship
from sqlalchemy import Column, Integer, String, DateTime, and_, \
    or_, INT, VARCHAR, UniqueConstraint, Boolean, Numeric, BigInteger, ForeignKey, func, Table, Index
from sqlalchemy.orm import relationship
from zing_product_backend.app_db.connections import Base
from zing_product_backend.core import common
from zing_product_backend.models import containment_model, auth_model
from sqlalchemy.dialects.postgresql import UUID, BIGINT


class SamplePlan(Base):
    __tablename__ = "sample_plan"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sample_plan_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True, unique=True)
    containment_rule_id: Mapped[int] = mapped_column(Integer, ForeignKey(containment_model.ContainmentRule.id))
    key_1: Mapped[str] = mapped_column(VARCHAR(), nullable=False, index=True)
    key_2: Mapped[str] = mapped_column(VARCHAR(), nullable=False, index=True)
    key_3: Mapped[str] = mapped_column(VARCHAR(), nullable=False, index=True)
    sample_type: Mapped[common.TpSampleType] = mapped_column(
        nullable=False)
    frequency_type: Mapped[common.TpFrequencyType] = mapped_column(nullable=True)
    frequency_value: Mapped[int] = mapped_column(Integer, nullable=True)
    must_include_seed_tail: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    plan_priority: Mapped[int] = mapped_column(Integer, nullable=False, comment='0 is the highest priority')

    updated_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_by = Column(UUID(as_uuid=True), ForeignKey(auth_model.User.id), nullable=False, index=True)
    updated_user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    containment_rule = relationship(containment_model.ContainmentRule)
    sample_tp_list: Mapped[List['AutoSampleTpStats']] = relationship('AutoSampleTpStats',
                                                                        back_populates='sample_plan')
    consider_unslicing_block: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    consider_unreached_block: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class AutoSampleLotStats(Base):
    __tablename__ = "auto_sample_lot_stats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    last_updated_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    lot_id: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, index=True, unique=True)
    oper: Mapped[str] = mapped_column(VARCHAR(10), nullable=False, index=True)
    tp_list: Mapped[List['AutoSampleTpStats']] = relationship('AutoSampleTpStats', back_populates='from_lot')
    virtual_factory: Mapped[str] = mapped_column(VARCHAR(10), nullable=False)


class AutoSampleTpStats(Base):
    __tablename__ = "auto_sample_tp_stats"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    last_updated_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    tp_id: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, index=True)
    oper: Mapped[str] = mapped_column(VARCHAR(10), nullable=False, index=True)
    picked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    pick_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    from_lot_id: Mapped[str] = mapped_column(VARCHAR(20), ForeignKey(AutoSampleLotStats.lot_id),
                                             nullable=False, index=True)
    from_sample_plan_id: Mapped[int] = mapped_column(Integer, ForeignKey(SamplePlan.id),
                                                     nullable=False, index=True)
    from_lot = relationship(AutoSampleLotStats, back_populates='tp_list')
    sample_plan = relationship(SamplePlan, back_populates='sample_tp_list')
