import pymongo
import socket
import datetime
from sqlalchemy import select
from zing_product_backend.app_db.mes_db_query import get_lot_sts, get_wafer_sts_by_lot_id
from zing_product_backend.core.common import VirtualFactory, ProductAllocationTransaction, ProductAllocationState
from zing_product_backend.app_db.connections import get_async_session
from zing_product_backend.models.auto_allocation_model import (
    AllocationLotStatus, AllocationLotState,
    AllocationTransactionHistory, AllocationWaferHistory, AllocationAnalysisHistory, AllocationWaferStatus
                                                               )


allocate_db_client = pymongo.MongoClient(socket.gethostbyname('AI01'), 27017)
l1w_db = allocate_db_client.auto_allocate_db
l2w_db = allocate_db_client.auto_allocate_db_l2w

# class AllocationLotStatus(Base):
#     __tablename__ = 'allocation_lot_status'
#     id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
#     lot_id: Mapped[str] = Column(VARCHAR(), nullable=False, index=True, unique=True)
#     current_oper = Column(VARCHAR(), nullable=False)
#     current_mat_id = Column(VARCHAR(), nullable=False)
#     target_mat_id = Column(VARCHAR(), nullable=True)
#     last_update_time: Mapped[datetime.datetime] = Column(DateTime, nullable=False)
#     last_comment: Mapped[str] = Column(VARCHAR())
#     virtual_factory = Column(VARCHAR(), nullable=False)
#     missing_char = Column(VARCHAR())
#     states: Mapped[List['AllocationLotState']] = relationship(
#         'AllocationLotState', back_populates='allocation_lot')
#     transaction_history: Mapped[List['AllocationTransactionHistory']] = relationship(
#         'AllocationLotHistory', back_populates='allocation_lot')
#     analysis_history: Mapped[List['AllocationAnalysisHistory']] = relationship(
#         'AllocationAnalysisHistory',
#         back_populates='allocation_lot')
#
#
# class AllocationTransactionHistory(Base):
#     __tablename__ = 'allocation_transaction_history'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     lot_id: Mapped[str] = Column(VARCHAR(), ForeignKey(AllocationLotStatus.lot_id), nullable=False, index=True)
#     transaction_code: Mapped[common.ProductAllocationTransaction] = Column(Enum(common.ProductAllocationTransaction),
#                                                                            nullable=False)
#     transaction_time: Mapped[datetime.datetime] = Column(DateTime, default=func.now(), nullable=False)
#     transaction_user_name = Column(VARCHAR(), ForeignKey(auth_model.User.user_name), nullable=False)
#     comment: Mapped[str] = Column(VARCHAR(), nullable=True)
#     oper: Mapped[str] = Column(VARCHAR(), nullable=False)
#     mat_id: Mapped[str] = Column(VARCHAR(), nullable=False)
#     target_mat_id: Mapped[str] = Column(VARCHAR(), nullable=True)
#     missing_char: Mapped[str] = Column(VARCHAR(), nullable=True)
#     states: Mapped[List['AllocationLotState']] = relationship('AllocationLotState', back_populates='transaction_history')
#     allocation_lot = relationship('AllocationLotStatus', back_populates='transaction_history')
#     wafer_history = relationship('AllocationWaferHistory', back_populates='transaction')
#
#
# class AllocationLotState(Base):
#     __tablename__ = 'allocation_lot_state'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     lot_id: Mapped[str] = Column(VARCHAR(), ForeignKey(AllocationLotStatus.lot_id), nullable=False, index=True)
#     state: Mapped[common.ProductAllocationState] = Column(Enum(common.ProductAllocationState), nullable=False)
#     state_delete_flag: Mapped[str] = Column(Boolean(), default=False)
#     state_time: Mapped[datetime.datetime] = Column(DateTime, default=func.now(), nullable=False)
#     transaction_id = Column(Integer(), ForeignKey(AllocationTransactionHistory.id))
#     allocation_lot = relationship('AllocationLotStatus', back_populates='states')
#
#
# class AllocationWaferStatus(Base):
#     __tablename__ = 'allocation_wafer_status'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     lot_status_id: Mapped[int] = Column(Integer(), ForeignKey(AllocationLotStatus.id), nullable=False, index=True)
#     wafer_id: Mapped[str] = Column(VARCHAR(), nullable=False, index=True, unique=True)
#     lot_id: Mapped[str] = Column(VARCHAR(), ForeignKey(AllocationLotStatus.lot_id), nullable=False, index=True)
#     missing_char = Column(VARCHAR())
#
#
# class AllocationWaferHistory(Base):
#     __tablename__ = 'allocation_wafer_history'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     wafer_id: Mapped[str] = Column(VARCHAR(), ForeignKey(AllocationWaferStatus.wafer_id), nullable=False, index=True)
#     transaction_id = Column(Integer(), ForeignKey(AllocationTransactionHistory.id), index=True)
#     transaction = relationship('AllocationTransactionHistory', back_populates='wafer_history')
#
#
# class AllocationAnalysisHistory(Base):
#     __tablename__ = 'allocation_analysis_history'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     lot_id: Mapped[str] = Column(VARCHAR(), ForeignKey(AllocationLotStatus.lot_id), nullable=False, index=True)
#     transaction_id = Column(Integer(), ForeignKey(AllocationTransactionHistory.id))
#     data = Column(JSONB, nullable=False)
#     analysis_time: Mapped[datetime.datetime] = Column(DateTime, default=func.now(), nullable=False)
#     allocation_lot = relationship('AllocationLotStatus', back_populates='analysis_history')
#


async def update_lot_main():
    current_time = datetime.datetime.now()
    async for s in get_async_session():
        for virtual_factory in VirtualFactory:
            if virtual_factory == VirtualFactory.ALL:
                continue
            if virtual_factory == VirtualFactory.L1W:
                db = l1w_db
            else:
                db = l2w_db

            data_dict_list = list(db.lot_allocation_history_new.find({
                'last_updated_time': {'$gt': current_time - datetime.timedelta(days=5)},
            }, {'lot_id': 1, 'target_material': 1, 'last_updated_time': 1}))
            for data_dict in data_dict_list:
                lot_sts = get_lot_sts(data_dict['lot_id'], virtual_factory)
                oper = lot_sts['oper']
                mat_id = lot_sts['mat_id']
                wafer_df = get_wafer_sts_by_lot_id(data_dict['lot_id'], virtual_factory)
                transaction = AllocationTransactionHistory(
                    lot_id=data_dict['lot_id'],
                    transaction_code=ProductAllocationTransaction.UPDATE,
                    transaction_user_name='admin',
                    oper=oper,
                    mat_id=mat_id,
                    target_mat_id=data_dict['target_material'],
                )
                lot_status = AllocationLotStatus(
                    transaction_id=transaction.id,
                    lot_id=data_dict['lot_id'],
                    current_oper=oper,
                    current_mat_id=mat_id,
                    target_mat_id=data_dict['target_material'],
                    last_update_time=data_dict['last_updated_time'],
                    virtual_factory=virtual_factory,
                )
                # check exist lot status
                stmt = select(AllocationLotStatus).where(AllocationLotStatus.lot_id == data_dict['lot_id'])
                exist_lot_status = (await s.execute(stmt)).scalars().one_or_none()
                if exist_lot_status is not None:
                    pass
                else:
                    s.add(lot_status)
                    await s.flush()

                s.add(transaction)
                await s.flush()
                await s.refresh(transaction)
                lot_status.transaction_id = transaction.id
                await s.merge(lot_status)
                await s.commit()
                state = AllocationLotState(
                    lot_id=data_dict['lot_id'],
                    state=ProductAllocationState.NORMAL,
                    transaction_id=transaction.id,
                )
                s.add(state)

                lot_history = AllocationLotState(
                    lot_id=data_dict['lot_id'],
                    state=ProductAllocationState.NORMAL,
                    transaction_id=transaction.id,
                )
                s.add(lot_history)

                for index, row in wafer_df.iterrows():
                    wafer_status = AllocationWaferStatus(
                        wafer_id=row['sublot_id'],
                        lot_id=row['lot_id'],
                    )
                    # check exist wafer status
                    stmt = select(AllocationWaferStatus).where(AllocationWaferStatus.wafer_id == row['sublot_id'])
                    exist_wafer_status = (await s.execute(stmt)).scalars().one_or_none()
                    if exist_wafer_status is not None:
                        pass
                    else:
                        s.add(wafer_status)
                    await s.flush()
                    wafer_history = AllocationWaferHistory(
                        wafer_id=row['sublot_id'],
                        transaction_id=transaction.id,
                    )
                    s.add(wafer_history)

            await s.commit()
