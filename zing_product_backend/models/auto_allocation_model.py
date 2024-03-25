from typing import TYPE_CHECKING, List, Dict
import datetime
from sqlalchemy import Column, Integer, String, DateTime, and_, \
    or_, INT, VARCHAR, UniqueConstraint, Boolean, Numeric, BigInteger, ForeignKey, func, Table, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Enum, text
from zing_product_backend.app_db.connections import Base
from zing_product_backend.core import common
from zing_product_backend.models import auth_model
from sqlalchemy.dialects.postgresql import UUID, BIGINT


class AllocationLotStatus(Base):
    __tablename__ = 'allocation_lot_status'
    lot_id: Mapped[str] = Column(VARCHAR(), primary_key=True)
    current_transaction_seq = Column(Integer(), nullable=True)
    current_oper = Column(VARCHAR(), nullable=False)
    current_mat_id = Column(VARCHAR(), nullable=False)
    target_mat_id = Column(VARCHAR(), nullable=True)
    last_updated_time: Mapped[datetime.datetime] = Column(DateTime, nullable=False, default=func.now())
    last_updated_user_name: Mapped[str] = Column(VARCHAR(), ForeignKey(auth_model.User.user_name), nullable=False)
    last_comment: Mapped[str] = Column(VARCHAR(), nullable=False, default='')
    last_transaction_code: Mapped[common.ProductAllocationTransaction] = Column(
            Enum(common.ProductAllocationTransaction), nullable=False)
    virtual_factory = Column(VARCHAR(), nullable=False)
    missing_char = Column(VARCHAR(), default='')
    states: Mapped[List['AllocationLotState']] = relationship(

        'AllocationLotState', back_populates='allocation_lot')
    transaction_history: Mapped[List['AllocationTransactionHistory']] = relationship(
        'AllocationTransactionHistory', back_populates='allocation_lot')
    analysis_history: Mapped[List['AllocationAnalysisHistory']] = relationship(
        'AllocationAnalysisHistory',
        back_populates='allocation_lot')


class AllocationTransactionHistory(Base):
    __tablename__ = 'allocation_transaction_history'
    lot_id: Mapped[str] = Column(VARCHAR(), ForeignKey(AllocationLotStatus.lot_id), primary_key=True)
    transaction_seq: Mapped[int] = Column(Integer, primary_key=True)
    transaction_code: Mapped[common.ProductAllocationTransaction] = Column(Enum(common.ProductAllocationTransaction),
                                                                           nullable=False)
    transaction_time: Mapped[datetime.datetime] = Column(DateTime, default=func.now(), nullable=False)
    transaction_user_name = Column(VARCHAR(), ForeignKey(auth_model.User.user_name), nullable=False)
    virtual_factory: Mapped[str] = Column(VARCHAR(), nullable=False)
    comment: Mapped[str] = Column(VARCHAR(), nullable=True)
    oper: Mapped[str] = Column(VARCHAR(), nullable=False)
    mat_id: Mapped[str] = Column(VARCHAR(), nullable=False)
    target_mat_id: Mapped[str] = Column(VARCHAR(), nullable=False)
    missing_char: Mapped[str] = Column(VARCHAR(), nullable=False)
    allocation_lot = relationship('AllocationLotStatus', back_populates='transaction_history')


class AllocationLotState(Base):
    __tablename__ = 'allocation_lot_state'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lot_id: Mapped[str] = Column(VARCHAR(), ForeignKey(AllocationLotStatus.lot_id), nullable=False, index=True)
    transaction_seq: Mapped[int] = Column(Integer, nullable=False)
    state: Mapped[common.ProductAllocationState] = Column(Enum(common.ProductAllocationState), nullable=False)
    state_delete_flag: Mapped[str] = Column(Boolean(), default=False)
    state_time: Mapped[datetime.datetime] = Column(DateTime, default=func.now(), nullable=False)
    allocation_lot = relationship('AllocationLotStatus', back_populates='states')


class AllocationWaferStatus(Base):
    __tablename__ = 'allocation_wafer_status'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lot_id: Mapped[str] = Column(VARCHAR(), ForeignKey(AllocationLotStatus.lot_id), nullable=False, index=True)
    wafer_id: Mapped[str] = Column(VARCHAR(), nullable=False, index=True, unique=True)
    missing_char = Column(VARCHAR())


class AllocationWaferHistory(Base):
    __tablename__ = 'allocation_wafer_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    wafer_id: Mapped[str] = Column(VARCHAR(), ForeignKey(AllocationWaferStatus.wafer_id), nullable=False, index=True)
    lot_id: Mapped[str] = Column(VARCHAR(), ForeignKey(AllocationLotStatus.lot_id), nullable=False, index=True)
    transaction_seq: Mapped[int] = Column(Integer, nullable=False)


class AllocationAnalysisHistory(Base):
    __tablename__ = 'allocation_analysis_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lot_id: Mapped[str] = Column(VARCHAR(), ForeignKey(AllocationLotStatus.lot_id), nullable=False, index=True)
    transaction_seq: Mapped[int] = Column(Integer, nullable=False)
    data = Column(JSONB, nullable=False)
    analysis_time: Mapped[datetime.datetime] = Column(DateTime, default=func.now(), nullable=False)
    allocation_lot = relationship('AllocationLotStatus', back_populates='analysis_history')
