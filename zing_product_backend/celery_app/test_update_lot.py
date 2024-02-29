import pymongo
import socket
import datetime
import asyncio
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
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


async def update_lot_main():
    while True:
        start_time = datetime.datetime.now()
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
                    stmt = select(AllocationLotStatus).where(
                        AllocationLotStatus.lot_id == data_dict['lot_id']).options(selectinload("*"))
                    exist_lot_status = (await s.execute(stmt)).scalars().one_or_none()
                    if not exist_lot_status:
                        transaction_seq = 1
                        lot_status = AllocationLotStatus(
                            lot_id=data_dict['lot_id'],
                            current_transaction_seq=transaction_seq,
                            current_oper=oper,
                            current_mat_id=mat_id,
                            target_mat_id=data_dict['target_material'],
                            last_updated_time=data_dict['last_updated_time'],
                            last_transaction_code=ProductAllocationTransaction.INFO_UPDATE,
                            last_comment='',
                            missing_char='',
                            last_updated_user_name='admin',
                            virtual_factory=virtual_factory,
                            states=[AllocationLotState(
                                lot_id=data_dict['lot_id'],
                                transaction_seq=1,
                                state=ProductAllocationState.NORMAL,
                            )],
                        )
                        s.add(lot_status)
                    else:
                        transaction_seq = exist_lot_status.current_transaction_seq + 1
                        lot_status = exist_lot_status
                        lot_status.current_oper = oper
                        lot_status.current_mat_id = mat_id
                        lot_status.target_mat_id = data_dict['target_material']
                        lot_status.last_updated_time = data_dict['last_updated_time']
                        lot_status.current_transaction_seq = transaction_seq

                    transaction = AllocationTransactionHistory(
                        lot_id=data_dict['lot_id'],
                        transaction_seq=lot_status.current_transaction_seq,
                        transaction_code=ProductAllocationTransaction.INFO_UPDATE,
                        transaction_user_name='admin',
                        missing_char='',
                        oper=oper,
                        mat_id=mat_id,
                        target_mat_id=data_dict['target_material'],
                        virtual_factory=virtual_factory,
                    )
                    s.add(transaction)

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
                            lot_id=row['lot_id'],
                            transaction_seq=transaction_seq,

                        )
                        s.add(wafer_history)

                await s.commit()
        await asyncio.sleep(800)


def change_to_normal(lot_orm: AllocationLotStatus, transaction_id):
    states: List[AllocationLotState] = lot_orm.states
    normal_exists = False
    for state in lot_orm.states:
        if not state.state_delete_flag and state.state == ProductAllocationState.NORMAL:
            normal_exists = True

    if normal_exists:
        # do nothing
        pass
    else:
        state = AllocationLotState(
            lot_id=lot_orm.lot_id,
            state=ProductAllocationState.NORMAL,
            transaction_id=transaction_id,
        )
        states.append(state)
    return None
