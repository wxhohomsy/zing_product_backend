from typing import List, Union, Literal, Optional, Set
from sqlalchemy.exc import DatabaseError
from zing_product_backend.core import common
from zing_product_backend.models import material_setting


def get_mat_group_id_set_from_mat_orm(mat_orm: material_setting.MatDef,
                                      target_group_type: common.MatGroupType
                                      ) -> Union[material_setting.MatGroupDef, None]:
    group_orm = None
    for group in mat_orm.groups:
        if target_group_type == group.group_type:
            if group_orm is not None:
                raise DatabaseError(f'mat has more than one group with same type: {target_group_type}')
            group_orm = group
    return group_orm
