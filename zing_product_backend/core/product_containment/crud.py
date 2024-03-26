from typing import Union, List, Dict, Any, Sequence, TYPE_CHECKING
import pandas as pd
from zing_product_backend.core import exceptions
from zing_product_backend.models import containment_model, general_settings
from zing_product_backend.app_db import connections, AppSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, lazyload
if TYPE_CHECKING:
    from zing_product_backend.core.product_containment.parser_core import containment_structure


async def get_available_puller_info_list() -> Sequence[general_settings.PullerInfo]:
    async for s in connections.get_async_session():
        stmt = select(general_settings.PullerInfo).options(lazyload('*'))
        puller_info_list = (await s.execute(stmt)).scalars().all()
        return puller_info_list


async def get_mat_yield_group_names() -> Sequence[str]:
    async for s in connections.get_async_session():
        stmt = select(general_settings.MatGroupDef.group_name).order_by(general_settings.MatGroupDef.group_name
                                                                        ).options(lazyload('*'))
        group_name_list = (await s.execute(stmt)).scalars().all()
        return group_name_list


def get_containment_rule_from_rule_id(rule_id: str) -> 'containment_structure.ContainmentRule':
    with AppSession() as s:
        stmt = select(containment_model.ContainmentRule).where(containment_model.ContainmentRule.id == rule_id)
        rule_orm = s.execute(stmt).one_or_none()
        if not rule_orm:
            raise exceptions.NotFoundError(f"Rule {rule_id} not found")
        return containment_structure.ContainmentRule(
            rule_orm=rule_orm,
        )


def get_yield_groups_by_mat_id(mat_id: str) -> str:
    with AppSession() as s:
        stmt = select(general_settings.MatDef).where(general_settings.MatDef.mat_id == mat_id)
        mat_orm = s.execute(stmt).fetchone()[0]
        if not mat_orm:
            raise exceptions.NotFoundError(f"Material {mat_id} not found")
        for mat_group in mat_orm.groups:
            if mat_group.group_type == 'yield_group':
                # assuming only one yield group per material
                return mat_group.group_name

        raise exceptions.NotFoundError(f"Yield group for material {mat_id} not found")


def get_ooc_spec_with_containment_id() -> pd.DataFrame:
    with AppSession() as s:
        stmt = select(general_settings.OOCRules)
        ooc_spec_df = pd.read_sql(stmt, s.bind)
        return ooc_spec_df
