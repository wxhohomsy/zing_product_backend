from sqlalchemy import select
from sqlalchemy.orm import selectinload
from zing_product_backend.app_db.connections import AsyncAppSession, AppSession
from zing_product_backend.core import exceptions
from zing_product_backend.models import general_settings


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
