import datetime
import time
from typing import List, Union, Optional, Dict, Any, Sequence, Literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import lazyload, selectinload
from zing_product_backend.core import common
from zing_product_backend.models import auth_model
from zing_product_backend.models.auto_allocation_model import (
    AllocationLotStatus, AllocationLotState,
    AllocationTransactionHistory, AllocationWaferHistory, AllocationAnalysisHistory, AllocationWaferStatus
    )
from . import schemas, utils


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
                transaction_id = state_orm.transaction_id
                if not state_orm.state_delete_flag:
                    transaction_orm = (await self.session.execute(select(AllocationTransactionHistory).filter(
                        AllocationTransactionHistory.id == transaction_id
                    ))).scalar_one()
                    if transaction_orm.comment is None:
                        state_comment = ''
                    else:
                        state_comment = transaction_orm.comment
                    state_list.append(schemas.AllocationState(
                        state_code=state_orm.state,
                        state_time=state_orm.state_time,
                        state_comment=state_comment,
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
                    last_update_time=orm.last_update_time,
                    last_update_user_name=orm.last_update_user_name,
                    last_comment=last_comment,
                    missing_chars=[],
                    transaction_id=orm.transaction_id,
                    wafer_count=25,
                    current_mat_id=orm.current_mat_id,
                    target_mat_id=orm.target_mat_id,
                    current_oper=orm.current_oper
                )
            )
        return return_list