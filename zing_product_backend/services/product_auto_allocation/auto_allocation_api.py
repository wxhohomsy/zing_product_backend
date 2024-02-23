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
from . import schemas
from . import crud


auto_allocation_router = APIRouter()


class LotStatsResponseModel(ResponseModel):
    data: List[schemas.LotStatus]


@auto_allocation_router.post("/lot_stats/{virtual_factory}", response_model=ResponseModel)
async def get_lot_stats(
        virtual_factory: VirtualFactory,
        session=Depends(get_async_session)
):
    db = crud.LotAllocationDataBase(session)
    lot_stats = await db.get_lot_allocation_info_list(virtual_factory)
    return LotStatsResponseModel(
        data=lot_stats,
        success=True,
    )


