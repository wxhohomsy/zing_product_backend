import typing
from typing import Union, Tuple, List
from fastapi import APIRouter, Depends
from zing_product_backend.reporting import system_log
from zing_product_backend.models import auth_model
from zing_product_backend.core.security.users import current_active_user
from zing_product_backend.core.security.schema import UserInfo
from zing_product_backend.app_db.connections import get_async_session
from zing_product_backend.core.common import ResponseModel, ErrorMessages, GENERAL_RESPONSE, VirtualFactory
from zing_product_backend.app_db import mes_db_query
from . import schemas, crud, dependents


auto_allocation_router = APIRouter()


class LotStatsListResponseModel(ResponseModel):
    data: List[schemas.LotStatus]


class LotHistoryResponse(ResponseModel):
    data: List[schemas.LotTransactionHistory]


@auto_allocation_router.get("/lot_stats/{virtual_factory}", response_model=LotStatsListResponseModel)
async def get_lot_stats(
        virtual_factory: VirtualFactory,
        user: UserInfo = Depends(current_active_user),
        session=Depends(get_async_session)
):
    db = crud.LotAllocationDataBase(session)
    lot_stats = await db.get_lot_allocation_info_list(virtual_factory)
    return LotStatsListResponseModel(
        data=lot_stats,
        success=True,
    )


@auto_allocation_router.post("/lot_transaction/hold_lot", response_model=ResponseModel)
async def hold_lot(
        hold_lot_data: schemas.HoldLot,
        user=Depends(dependents.current_product_allocation_state_change_user),
        session=Depends(get_async_session)
):
    db = crud.LotAllocationDataBase(session)
    await db.hold_lot(hold_lot_data, user)
    return ResponseModel(
        data=hold_lot_data,
        success=True,
        success_message=f'hold lot {hold_lot_data.lot_id} success'
    )


@auto_allocation_router.post("/lot_transaction/release_lot", response_model=ResponseModel)
async def release_lot(
        release_lot_data: schemas.ReleaseLot,
        user=Depends(dependents.current_product_allocation_state_change_user),
        session=Depends(get_async_session)
):
    db = crud.LotAllocationDataBase(session)
    await db.release_lot(release_lot_data, user)
    return ResponseModel(
        success=True,
        success_message=f'release lot {release_lot_data.lot_id} success'
    )


@auto_allocation_router.get("/lot_query/history/{lot_id}", response_model=LotHistoryResponse)
async def get_lot_transaction_history(
        lot_id: str,
        session=Depends(get_async_session)
):
    db = crud.LotAllocationDataBase(session)
    history_list = await db.get_lot_transaction_history(lot_id)
    return LotHistoryResponse(
        data=history_list,
        success=True,
    )
