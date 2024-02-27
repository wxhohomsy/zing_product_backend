import datetime
import time
from typing import List, Union, Optional, Dict, Any, Sequence, Literal, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, text
from sqlalchemy.orm import lazyload, selectinload
from zing_product_backend.core import common, exceptions
from zing_product_backend.models import auth_model
from zing_product_backend.models.auto_allocation_model import (
    AllocationLotStatus, AllocationLotState,
    AllocationTransactionHistory, AllocationWaferHistory, AllocationAnalysisHistory, AllocationWaferStatus
)
from . import schemas, utils


def create_new_non_allocate_transaction(
        transaction_code: common.ProductAllocationTransaction, lot_orm: AllocationLotStatus, comment: str,
        user: auth_model.User) -> Tuple[AllocationLotState, AllocationTransactionHistory]:
    current_seq = lot_orm.current_transaction_seq
    new_seq = current_seq + 1
    new_transaction = AllocationTransactionHistory(
        lot_id=lot_orm.lot_id,
        mat_id=lot_orm.current_mat_id,
        target_mat_id=lot_orm.target_mat_id,
        missing_char=lot_orm.missing_char,
        transaction_code=transaction_code,
        transaction_seq=new_seq,
        oper=lot_orm.current_oper,
        transaction_time=datetime.datetime.now(),
        transaction_user_name=user.user_name,
        comment=comment
    )
    return new_transaction


async def get_current_lot_orm(lot_id, transaction_init_seq: int,  session: AsyncSession, use_selectinload=False
                              ) -> AllocationLotStatus:
    if use_selectinload:
        stmt = select(AllocationLotStatus).filter(AllocationLotStatus.lot_id == lot_id).options(selectinload("*"))
    else:
        stmt = select(AllocationLotStatus).filter(AllocationLotStatus.lot_id == lot_id)
    result = await session.execute(stmt)
    lot_orm: AllocationLotStatus = result.scalar_one_or_none()
    if lot_orm is None:
        raise exceptions.NotFoundError(f'lot {lot_id} not found')
    else:
        if lot_orm.current_transaction_seq != transaction_init_seq:
            raise exceptions.OutDatedDataError(f'lot seq not match ({lot_orm.current_transaction_seq}'
                                               f' vs {transaction_init_seq}),'
                                               f' please refresh and try again')
        else:
            return lot_orm


class LotAllocationDataBase:
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def get_lot_allocation_info_list(self, v_factory: common.VirtualFactory) -> Sequence[schemas.LotStatus]:
        stmt = select(AllocationLotStatus).filter(AllocationLotStatus.current_oper == '2920').options(
            selectinload(AllocationLotStatus.states))
        if v_factory == common.VirtualFactory.ALL:
            pass
        else:
            stmt = stmt.filter(AllocationLotStatus.virtual_factory == v_factory.value)
        result = await self.session.execute(stmt)
        orm_list: Sequence[AllocationLotStatus] = result.scalars().all()
        return_list: List[schemas.LotStatus] = []
        for orm in orm_list:
            state_orms: Sequence[AllocationLotState] = orm.states
            state_list: schemas.LotStatus = []
            for state_orm in state_orms:
                transaction_seq = state_orm.transaction_seq
                if not state_orm.state_delete_flag:
                    transaction_orm = (await self.session.execute(select(AllocationTransactionHistory).filter(
                        and_(AllocationTransactionHistory.transaction_seq == transaction_seq,
                             AllocationTransactionHistory.lot_id == orm.lot_id
                             )
                    ))).scalar_one()
                    if transaction_orm.comment is None:
                        state_comment = ''
                    else:
                        state_comment = transaction_orm.comment
                    state_list.append(schemas.AllocationState(
                        state_code=state_orm.state,
                        state_time=state_orm.state_time,
                        state_comment=state_comment,
                        id=state_orm.id
                    ))

            if orm.last_comment is None:
                last_comment = ''
            else:
                last_comment = orm.last_comment
            return_list.append(
                schemas.LotStatus(
                    lot_id=orm.lot_id,
                    virtual_factory=common.VirtualFactory(orm.virtual_factory),
                    active_states=state_list,
                    last_updated_time=orm.last_updated_time,
                    last_updated_user_name=orm.last_updated_user_name,
                    last_comment=last_comment,
                    missing_chars=[],
                    current_transaction_seq=orm.current_transaction_seq,
                    wafer_count=25,
                    current_mat_id=orm.current_mat_id,
                    target_mat_id=orm.target_mat_id,
                    current_oper=orm.current_oper
                )
            )
        return return_list

    async def get_lot_sts(self, lot_id: str) -> schemas.LotStatus:
        stmt = select(AllocationLotStatus).filter(AllocationLotStatus.current_oper == '2920').options(
            selectinload(AllocationLotStatus.states))
        lot_status_orm = (await self.session.execute(stmt)).scalar_one_or_none()
        if lot_status_orm is None:
            raise exceptions.NotFoundError(f'lot {lot_id} not found')
        else:
            state_orms: Sequence[AllocationLotState] = lot_status_orm.states
            state_list: schemas.LotStatus = []
            for state_orm in state_orms:
                transaction_seq = state_orm.transaction_seq
                if not state_orm.state_delete_flag:
                    transaction_orm = (await self.session.execute(select(AllocationTransactionHistory).filter(
                        and_(AllocationTransactionHistory.transaction_seq == transaction_seq,
                             AllocationTransactionHistory.lot_id == lot_id
                             )
                    ))).scalar_one()
                    if transaction_orm.comment is None:
                        state_comment = ''
                    else:
                        state_comment = transaction_orm.comment
                    state_list.append(schemas.AllocationState(
                        state_code=state_orm.state,
                        state_time=state_orm.state_time,
                        state_comment=state_comment,
                        id=state_orm.id
                    ))

            if lot_status_orm.last_comment is None:
                last_comment = ''
            else:
                last_comment = lot_status_orm.last_comment

            return schemas.LotStatus(
                lot_id=lot_status_orm.lot_id,
                virtual_factory=common.VirtualFactory(lot_status_orm.virtual_factory),
                active_states=state_list,
                last_updated_time=lot_status_orm.last_updated_time,
                last_updated_user_name=lot_status_orm.last_updated_user_name,
                last_comment=last_comment,
                missing_chars=[],
                current_transaction_seq=lot_status_orm.current_transaction_seq,
                wafer_count=25,
                current_mat_id=lot_status_orm.current_mat_id,
                target_mat_id=lot_status_orm.target_mat_id,
                current_oper=lot_status_orm.current_oper
            )

    async def get_lot_transaction_history(self, lot_id: str) -> Sequence[schemas.LotTransaction]:
        stmt = select(AllocationTransactionHistory).filter(AllocationTransactionHistory.lot_id == lot_id)
        result = await self.session.execute(stmt)
        orm_list: Sequence[AllocationTransactionHistory] = result.scalars().all()
        return_list: List[schemas.LotTransaction] = []
        for orm in orm_list:
            if orm.comment is None:
                comment = ''
            else:
                comment = orm.comment

            return_list.append(
                schemas.LotTransaction(
                    lot_id=orm.lot_id,
                    transaction_code=orm.transaction_code,
                    transaction_time=orm.transaction_time,
                    transaction_seq=orm.transaction_seq,
                    comment=comment,
                    oper=orm.oper,
                    mat_id=orm.mat_id,
                    target_mat_id=orm.target_mat_id,
                    missing_char=orm.missing_char,
                    state_code_list=[]
                )
            )
        return return_list

    async def hold_lot(self, hold_lot_data: schemas.HoldLot, user: auth_model.User):
        lot_orm = await get_current_lot_orm(hold_lot_data.lot_id, hold_lot_data.current_transaction_seq, self.session)
        new_transaction_seq = hold_lot_data.current_transaction_seq + 1
        new_transaction = create_new_non_allocate_transaction(
            common.ProductAllocationTransaction.HOLD, lot_orm, hold_lot_data.comment, user
        )
        new_state = AllocationLotState(
            lot_id=lot_orm.lot_id,
            state=common.ProductAllocationState.HOLD,
            state_time=datetime.datetime.now(),
            state_user_name=user.user_name,
            transaction_seq=new_transaction_seq
        )
        self.session.add(new_state)
        self.session.add(new_transaction)
        lot_orm.current_transaction_seq = new_transaction_seq
        await self.session.merge(lot_orm)
        await self.session.commit()

    async def release_lot(self, release_lot_data: schemas.ReleaseLot, user: auth_model.User):
        lot_orm = await get_current_lot_orm(release_lot_data.lot_id, release_lot_data.current_transaction_seq,
                                            self.session, use_selectinload=True)
        new_transaction_seq = release_lot_data.current_transaction_seq + 1
        new_transaction = create_new_non_allocate_transaction(
            common.ProductAllocationTransaction.RELEASE, lot_orm, release_lot_data.comment, user
        )
        exist_hold_state_stmt = select(AllocationLotState).filter(
            and_(AllocationLotState.id == release_lot_data.hold_id,
                 AllocationLotState.lot_id == release_lot_data.lot_id,
                 AllocationLotState.state_delete_flag == False
                 )
        )
        lot_orm.current_transaction_seq = new_transaction_seq

        hold_state_orm = (await self.session.execute(exist_hold_state_stmt)).scalar_one_or_none()
        if hold_state_orm is None:
            raise exceptions.NotFoundError(f'hold state not found for {release_lot_data.lot_id}')
        else:
            hold_state_orm.state_delete_flag = True

        self.session.add(new_transaction)

