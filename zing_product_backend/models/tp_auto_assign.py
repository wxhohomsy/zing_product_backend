import datetime
from typing import List, Dict, Set, Literal, Union
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr, relationship
from sqlalchemy import VARCHAR, ForeignKey, DateTime, Boolean, Integer, String, Table
from sqlalchemy import Column, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, BIGINT
from zing_product_backend.app_db.connections import Base
from zing_product_backend.core import common


class BaseSamplePlan(Base):
    __tablename__ = "sample_plan"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sample_plan_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True, unique=True)

    key_1: Mapped[str] = mapped_column(VARCHAR(), nullable=False, index=True)
    key_2: Mapped[str] = mapped_column(VARCHAR(), nullable=False, index=True)
    key_3: Mapped[str] = mapped_column(VARCHAR(), nullable=False, index=True)
    frequency_type: Mapped[common.TpFrequencyType] = mapped_column(String(),
                                                                   comment='by_ingot/by_segment/every_fixed_mm/wafer_direct',
                                                                   nullable=True)
    frequency_value: Mapped[int] = mapped_column(Integer, nullable=True)
    must_include_seed_tail: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    plan_priority: Mapped[int] = mapped_column(Integer, nullable=False, comment='0 is the highest priority')
    triggered_tp_list: Mapped[List['AutoSampleTpStats']] = relationship('TpAutoAssignTpStats',
                                                                          back_populates='sample_plan')


class AutoSampleLotStats(Base):
    __tablename__ = "auto_sample_lot_stats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    last_updated_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    lot_id: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, index=True)
    oper: Mapped[str] = mapped_column(VARCHAR(10), nullable=False, index=True)
    tp_list: Mapped[List['AutoSampleTpStats']]


class AutoSampleTpStats(Base):
    __tablename__ = "auto_sample_tp_stats"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    last_updated_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    tp_id: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, index=True)
    oper: Mapped[str] = mapped_column(VARCHAR(10), nullable=False, index=True)
    picked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    pick_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    from_lot_id: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, index=True, )

    from_lot = relationship(AutoSampleLotStats, back_populates='tp_list')
    sample_plan = relationship(BaseSamplePlan, back_populates='sample_tp_list')
