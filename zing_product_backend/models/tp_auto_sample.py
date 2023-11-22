from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr, relationship
from sqlalchemy import VARCHAR, ForeignKey, DateTime, Boolean, Integer, String, Table
from zing_product_backend.app_db.connections import Base
from sqlalchemy import Column, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, BIGINT
from zing_product_backend.app_db.connections import Base


class SampleRule(Base):
    pass


class SampleGroup(Base):
    pass


class SampleGroupRule(Base):
    pass


class MaterialDef(Base):
    pass


class FutureSampleAction(Base):
    __tablename__ = "future_sample_action"
    __table_args__ = {'schema': 'tp_sample'}
    future_sample_action_id = Column(Integer, primary_key=True, autoincrement=True)
    ingot_id = Column(String(20), nullable=False, index=True)
    tp_flow_id = mapped_column(String(20), nullable=False)
    tp_code_id = mapped_column(String(20), nullable=False)
    frequency_type = mapped_column(String(), comment='by_ingot/by_segment/every_fixed_mm')
    frequency_value = mapped_column(Integer, nullable=True)


class CustomSampleFrequency(Base):
    __tablename__ = "custom_sample_frequency"
    __table_args__ = {'schema': 'tp_sample'}
    custom_sample_frequency_id = Column(Integer, primary_key=True, autoincrement=True)
    custom_sample_frequency_name = Column(String(50), nullable=False, index=True)


class SamplePlan(Base):
    __tablename__ = "sample_plan"
    __table_args__ = {'schema': 'tp_sample'}
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    sample_plan_name = mapped_column(String(50), nullable=False, index=True, unique=True)
    tp_flow_id = mapped_column(String(20), nullable=False)
    tp_code_id = mapped_column(String(20), nullable=False)
    sample_type = mapped_column(String(20), comment='seed_tail/frequency/custom')
    frequency_type = mapped_column(String(), comment='by_ingot/by_segment/every_fixed_mm', nullable=True)
    frequency_value = mapped_column(Integer, nullable=True)
    must_include_seed_tail = mapped_column(Boolean, nullable=False)
    plan_priority = mapped_column(Integer, nullable=False, comment='0 is the highest priority')


class MaterialSamplePlan(Base):
    __tablename__ = "mat_sample_relation"
    __table_args__ = {'schema': 'tp_sample'}
    serial_number = mapped_column(Integer, primary_key=True, autoincrement=True)
    mat_type = mapped_column(String(), comment='material_id/material_group')
    mat = mapped_column(String(20), index=True)
    sample_plan_id = mapped_column(ForeignKey(SamplePlan.sample_plan_id), index=True)