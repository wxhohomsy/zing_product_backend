from typing import Union, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from zing_product_backend.models import containment_model, general_settings
from zing_product_backend.app_db import connections
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, lazyload


async def get_available_puller_info_list() -> List[general_settings.PullerInfo]:
    async for s in connections.get_async_session():
        stmt = select(general_settings.PullerInfo).options(lazyload('*'))
        puller_info_list = (await s.execute(stmt)).scalars().all()
        return puller_info_list


async def get_mat_yield_group_names() -> List[str]:
    async for s in connections.get_async_session():
        stmt = select(general_settings.MatGroupDef.group_name).order_by(general_settings.MatGroupDef.group_name
                                                                        ).options(lazyload('*'))
        group_name_list = (await s.execute(stmt)).scalars().all()
        return group_name_list

