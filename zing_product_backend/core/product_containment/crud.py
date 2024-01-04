from typing import Union, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from zing_product_backend.models import containment_model
from zing_product_backend.app_db import connections
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, lazyload


async def get_containment_base_rule_by_id(base_rule_id: int, lazy_load=False,
                                          async_session: Union[AsyncSession, None] = None) -> \
        containment_model.ContainmentBaseRule:
    stmt = select(containment_model.ContainmentBaseRule).filter(
        containment_model.ContainmentBaseRule.id == base_rule_id
    )
    if lazy_load:
        stmt = stmt.options(lazyload('*'))
    else:
        stmt = stmt.options(selectinload('*'))

    if async_session is None:
        async for s in connections.get_async_session():
            base_rule = (await s.execute(stmt)).scalars().one_or_none()
    else:
        base_rule = (await async_session.execute(stmt)).scalars().one_or_none()
    return base_rule
