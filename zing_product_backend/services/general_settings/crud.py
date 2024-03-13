import time
from typing import List, Union, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import lazyload
from zing_product_backend.services.general_settings import schemas
from zing_product_backend.models import general_settings
from zing_product_backend.core import common
from zing_product_backend.services.general_settings import util_functions
from zing_product_backend.models.auth_model import User
from zing_product_backend.models.containment_model import ContainmentRule
from zing_product_backend.models.general_settings import OOCRules, ContainmentRule
from datetime import datetime
from zing_product_backend.core.security.schema import UserInfo
from sqlalchemy import select, update, delete


class DatabaseError(Exception):
    pass


class SettingsDataBase:
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def get_all_mat_info_restrict_by_group_type(self, group_type: common.MatGroupType
                                                      ) -> List[schemas.MatGroupInfo]:
        stmt = select(general_settings.MatDef).where(general_settings.MatDef.delete_flag == False)
        mat_info_list: List[schemas.MatInfoByGroupType] = []
        mat_orm_list: List[general_settings.MatDef] = (await self.session.execute(stmt)).scalars().all()
        for mat_orm in mat_orm_list:
            group_name = None
            group_id = None
            groups = mat_orm.groups
            for group in groups:
                if group.group_type == group_type:
                    group_name = group.group_name
                    group_id = group.id
                    break
            mat_info = schemas.MatInfoByGroupType(
                id=mat_orm.id,
                mat_id=mat_orm.mat_id,
                mat_description=mat_orm.mat_description,
                group_name=group_name,
                group_id=group_id,
                group_type=group_type,
                mat_base_type=mat_orm.mat_base_type,
                created_time=mat_orm.created_time,
                updated_time=mat_orm.updated_time,
                updated_by=mat_orm.updated_by,
                mat_type=mat_orm.mat_type,
                mat_grp_1=mat_orm.mat_grp_1,
                mat_grp_2=mat_orm.mat_grp_2,
                mat_grp_3=mat_orm.mat_grp_3,
                mat_grp_4=mat_orm.mat_grp_4,
                mat_grp_5=mat_orm.mat_grp_5,
                mat_grp_6=mat_orm.mat_grp_6,
                mat_grp_7=mat_orm.mat_grp_7,
                mat_grp_8=mat_orm.mat_grp_8,
                first_flow=mat_orm.first_flow,
            )
            mat_info_list.append(mat_info)
        return mat_info_list

    async def get_mat_group_detail(self, mat_group_id: int):
        stmt = select(general_settings.MatGroupDef).where(general_settings.MatGroupDef.id == mat_group_id)
        mat_group_orm = (await self.session.execute(stmt)).scalars().first()
        if mat_group_orm is None:
            raise DatabaseError(f'mat_group_id: {mat_group_id} not found')
        else:
            mat_info_list = []
            for mat_orm in mat_group_orm.materials:
                mat_info_list.append(
                    schemas.MatInfoByGroupType(
                        id=mat_orm.id,
                        mat_id=mat_orm.mat_id,
                        mat_description=mat_orm.mat_description,
                        group_name=mat_group_orm.group_name,
                        group_id=mat_group_orm.id,
                        group_type=mat_group_orm.group_type,
                        mat_base_type=mat_orm.mat_base_type,
                        created_time=mat_orm.created_time,
                        updated_time=mat_orm.updated_time,
                        updated_by=mat_orm.updated_by,
                        mat_type=mat_orm.mat_type,
                        mat_grp_1=mat_orm.mat_grp_1,
                        mat_grp_2=mat_orm.mat_grp_2,
                        mat_grp_3=mat_orm.mat_grp_3,
                        mat_grp_4=mat_orm.mat_grp_4,
                        mat_grp_5=mat_orm.mat_grp_5,
                        mat_grp_6=mat_orm.mat_grp_6,
                        mat_grp_7=mat_orm.mat_grp_7,
                        mat_grp_8=mat_orm.mat_grp_8,
                        first_flow=mat_orm.first_flow,
                    )
                )
            mat_group_info = schemas.MatGroupDetail(
                id=mat_group_id,
                group_name=mat_group_orm.group_name,
                group_type=mat_group_orm.group_type,
                description=mat_group_orm.group_description,
                mat_info_list=mat_info_list,
                updated_by=mat_group_orm.updated_by,
                updated_time=mat_group_orm.updated_time
            )
            return mat_group_info

    async def get_mat_info_restrict_by_group_type(self, mat_id: int, group_type: common.MatGroupType
                                                  ) -> schemas.MatInfoByGroupType:
        stmt = select(general_settings.MatDef).where(general_settings.MatDef.id == mat_id)
        mat_orm = (await self.session.execute(stmt)).scalars().first()
        if mat_orm is None:
            raise DatabaseError(f'mat_id: {mat_id} not found')
        else:
            group_orm = util_functions.get_mat_group_id_set_from_mat_orm(mat_orm, group_type)
            if not group_orm:
                group_name = None
                group_id = None
                group_type = None
            else:
                group_name = group_orm.group_name
                group_id = group_orm.id
                group_type = group_orm.group_type

            mat_info = schemas.MatInfoByGroupType(
                id=mat_orm.id,
                mat_id=mat_orm.mat_id,
                mat_description=mat_orm.mat_description,
                group_name=group_name,
                group_id=group_id,
                group_type=group_type,
                mat_base_type=mat_orm.mat_base_type,
                created_time=mat_orm.created_time,
                updated_time=mat_orm.updated_time,
                updated_by=mat_orm.updated_by,
                mat_type=mat_orm.mat_type,
                mat_grp_1=mat_orm.mat_grp_1,
                mat_grp_2=mat_orm.mat_grp_2,
                mat_grp_3=mat_orm.mat_grp_3,
                mat_grp_4=mat_orm.mat_grp_4,
                mat_grp_5=mat_orm.mat_grp_5,
                mat_grp_6=mat_orm.mat_grp_6,
                mat_grp_7=mat_orm.mat_grp_7,
                mat_grp_8=mat_orm.mat_grp_8,
                first_flow=mat_orm.first_flow,
            )
            return mat_info

    async def update_mat_info(self, to_update_mat_info_list: List[schemas.UpdateMatInfoByGroupTypeBase],
                              group_type: common.MatGroupType, usr):
        id_dict = {}
        for update_mat_info in to_update_mat_info_list:
            _id = update_mat_info.id
            id_dict[_id] = update_mat_info

        stmt = select(general_settings.MatDef).where(general_settings.MatDef.id.in_(tuple(id_dict.keys())))
        mat_orm_list: List[general_settings.MatDef] = (await self.session.execute(stmt)).scalars().all()
        for mat_orm in mat_orm_list:
            _id = mat_orm.id
            update_mat_info = id_dict[mat_orm.id]
            group_id = update_mat_info.group_id
            mat_orm.updated_by = usr.user_name
            if group_id is not None:
                new_group_orm = await self.session.get(general_settings.MatGroupDef, group_id)
                exits_group_orm = util_functions.get_mat_group_id_set_from_mat_orm(mat_orm,
                                                                                   group_type)
                if exits_group_orm is not None:
                    mat_orm.groups.remove(exits_group_orm)
                mat_orm.groups.append(new_group_orm)
            else:
                exits_group_orm = util_functions.get_mat_group_id_set_from_mat_orm(mat_orm,
                                                                                   group_type)
                if exits_group_orm is not None:
                    mat_orm.groups.remove(exits_group_orm)

        await self.session.commit()
        return None

    async def get_all_mat_group_detail(self, mat_group_type: common.MatGroupType) -> List[schemas.MatGroupDetail]:
        stmt = select(general_settings.MatGroupDef).where(general_settings.MatGroupDef.group_type == mat_group_type)
        mat_group_list: List[schemas.MatGroupDetail] = []
        mat_group_orm_list: List[general_settings.MatGroupDef] = (await self.session.execute(stmt)).scalars().all()
        for mat_group_orm in mat_group_orm_list:
            mat_info_list = []
            for mat_orm in mat_group_orm.materials:
                mat_info_list.append(
                    schemas.MatInfoByGroupType(
                        id=mat_orm.id,
                        mat_id=mat_orm.mat_id,
                        mat_description=mat_orm.mat_description,
                        group_name=mat_group_orm.group_name,
                        group_id=mat_group_orm.id,
                        group_type=mat_group_orm.group_type,
                        mat_base_type=mat_orm.mat_base_type,
                        created_time=mat_orm.created_time,
                        updated_time=mat_orm.updated_time,
                        updated_by=mat_orm.updated_by,
                        mat_type=mat_orm.mat_type,
                        mat_grp_1=mat_orm.mat_grp_1,
                        mat_grp_2=mat_orm.mat_grp_2,
                        mat_grp_3=mat_orm.mat_grp_3,
                        mat_grp_4=mat_orm.mat_grp_4,
                        mat_grp_5=mat_orm.mat_grp_5,
                        mat_grp_6=mat_orm.mat_grp_6,
                        mat_grp_7=mat_orm.mat_grp_7,
                        mat_grp_8=mat_orm.mat_grp_8,
                        first_flow=mat_orm.first_flow,
                    )
                )
            mat_group_info = schemas.MatGroupDetail(
                group_name=mat_group_orm.group_name,
                group_type=mat_group_orm.group_type,
                description=mat_group_orm.group_description,
                mat_info_list=mat_info_list,
                updated_by=mat_group_orm.updated_by,
                updated_time=mat_group_orm.updated_time,
                id=mat_group_orm.id
            )
            mat_group_list.append(mat_group_info)
        return mat_group_list

    async def get_all_mat_group_info(self, mat_group_type: common.MatGroupType) -> List[schemas.MatGroupInfo]:
        stmt = select(general_settings.MatGroupDef).where(
            general_settings.MatGroupDef.group_type == mat_group_type).options(
            lazyload('*'))
        mat_group_info_list: List[schemas.MatGroupDetail] = []
        mat_group_orm_list: List[general_settings.MatGroupDef] = (await self.session.execute(stmt)).scalars().all()
        for mat_group_orm in mat_group_orm_list:
            mat_group_info_list.append(schemas.MatGroupInfo(
                group_type=mat_group_type,
                group_name=mat_group_orm.group_name,
                description=mat_group_orm.group_description,
                updated_by=mat_group_orm.updated_by,
                updated_time=mat_group_orm.updated_time,
                id=mat_group_orm.id
            ))
        return mat_group_info_list

    async def create_group(self, to_create_group: schemas.CreateMatGroup,
                           group_type: common.MatGroupType, usr: User) -> schemas.MatGroupInfo:
        group_name = to_create_group.group_name
        description = to_create_group.description

        stmt = select(general_settings.MatGroupDef).where(
            and_(general_settings.MatGroupDef.group_name == group_name,
                 general_settings.MatGroupDef.group_type == group_type)).options(
            lazyload('*'))
        if (await self.session.execute(stmt)).scalars().first() is not None:
            raise DatabaseError(f'group name: {group_name} for {group_type} already exists')

        group_orm = general_settings.MatGroupDef(group_name=group_name, group_type=group_type,
                                                 group_description=description,
                                                 created_by=usr.user_name,
                                                 updated_by=usr.user_name
                                                 )

        self.session.add(group_orm)
        await self.session.commit()
        await self.session.refresh(group_orm)
        return schemas.MatGroupInfo(
            group_type=group_orm.group_type,
            group_name=group_orm.group_name,
            description=group_orm.group_description,
            updated_by=group_orm.updated_by,
            updated_time=group_orm.updated_time,
            id=group_orm.id
        )

    async def update_group(self, to_update_group: schemas.UpdateMatGroup) -> schemas.MatGroupInfo:
        group_id = to_update_group.group_id
        group_name = to_update_group.group_name
        description = to_update_group.description
        group_orm = await self.session.get(general_settings.MatGroupDef, group_id, options=[lazyload('*')])
        if group_orm is None:
            raise DatabaseError(f'group id: {group_id} not found')
        else:
            if group_name is not None:
                group_orm.group_name = group_name
            if description is not None:
                group_orm.group_description = description
            group_orm.updated_by = group_orm.updated_by

        await self.session.commit()
        await self.session.refresh(group_orm)
        return schemas.MatGroupInfo(
            group_type=group_orm.group_type,
            group_name=group_orm.group_name,
            description=group_orm.group_description,
            updated_by=group_orm.updated_by,
            updated_time=group_orm.updated_time,
            id=group_orm.id
        )

    async def delete_group(self, to_delete_group: schemas.DeleteMatGroup) \
            -> schemas.MatGroupDetail:
        group_id = to_delete_group.group_id
        stmt = select(general_settings.MatGroupDef).where(
            and_(
                general_settings.MatGroupDef.id == group_id,
            )
        )
        group_orm = (await self.session.execute(stmt)).scalars().first()
        if group_orm is None:
            raise DatabaseError(f'group id: {group_id} not found')
        else:
            mat_info_list = []
            for mat_orm in group_orm.materials:
                mat_info_list.append(
                    schemas.MatInfoByGroupType(
                        id=mat_orm.id,
                        mat_id=mat_orm.mat_id,
                        mat_description=mat_orm.mat_description,
                        group_name=group_orm.group_name,
                        group_id=group_orm.id,
                        group_type=group_orm.group_type,
                        mat_base_type=mat_orm.mat_base_type,
                        created_time=mat_orm.created_time,
                        updated_time=mat_orm.updated_time,
                        updated_by=mat_orm.updated_by,
                        mat_type=mat_orm.mat_type,
                        mat_grp_1=mat_orm.mat_grp_1,
                        mat_grp_2=mat_orm.mat_grp_2,
                        mat_grp_3=mat_orm.mat_grp_3,
                        mat_grp_4=mat_orm.mat_grp_4,
                        mat_grp_5=mat_orm.mat_grp_5,
                        mat_grp_6=mat_orm.mat_grp_6,
                        mat_grp_7=mat_orm.mat_grp_7,
                        mat_grp_8=mat_orm.mat_grp_8,
                        first_flow=mat_orm.first_flow,
                    )
                )
            deleted_group_orm = schemas.MatGroupDetail(
                id=group_orm.id,
                group_name=group_orm.group_name,
                group_type=group_orm.group_type,
                description=group_orm.group_description,
                mat_info_list=mat_info_list,
                updated_by=group_orm.updated_by,
                updated_time=group_orm.updated_time
            )
            await self.session.delete(group_orm)
        await self.session.commit()
        return deleted_group_orm


class OOCRulesCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_ooc_rule(self, ooc_rule_data: schemas.OOCRuleCreate, user: UserInfo) -> OOCRules:
        select_stmt = select(OOCRules).where(and_(OOCRules.containment_rule_id == ooc_rule_data.containment_rule_id,
                                                  OOCRules.spec_id == ooc_rule_data.spec_id,
                                                  OOCRules.rule_delete_flag == False))
        if (await self.session.execute(select_stmt)).scalars().first() is not None:
            info = select(ContainmentRule.rule_name).where(ContainmentRule.id == ooc_rule_data.containment_rule_id)
            raise DatabaseError(f'ooc rule: {ooc_rule_data.spec_id} for {info} already exists')
        new_ooc_rule = OOCRules(
            containment_rule_id=ooc_rule_data.containment_rule_id,
            spec_id=ooc_rule_data.spec_id,
            lower_limit=ooc_rule_data.lower_limit,
            upper_limit=ooc_rule_data.upper_limit,
            create_user_name=user.user_name,
            updated_user_name=user.user_name,
            create_time=datetime.now(),
            updated_time=datetime.now(),
            rule_delete_flag=False
        )
        self.session.add(new_ooc_rule)
        await self.session.commit()
        await self.session.refresh(new_ooc_rule)
        return new_ooc_rule

    async def update_ooc_rule(self, update_data: schemas.OOCRuleUpdate, user: UserInfo) -> None:
        result = self.get_ooc_rule_by_id(update_data.id)
        if result is None:
            raise DatabaseError(f'ooc rule id: {update_data.id} not found')
        update_stmt = update(OOCRules).where(OOCRules.id == update_data.id).values(
            lower_limit=update_data.lower_limit,
            upper_limit=update_data.upper_limit,
            updated_time=datetime.now(),
            updated_user_name=user.user_name
        )
        await self.session.execute(update_stmt)
        await self.session.commit()

    async def delete_ooc_rule(self, ooc_rule_id: int, user: UserInfo) -> None:
        result = self.get_ooc_rule_by_id(ooc_rule_id)
        if result is None:
            raise DatabaseError(f'ooc rule id: {ooc_rule_id} not found')
        delete_stmt = update(OOCRules).where(OOCRules.id == ooc_rule_id).values(
            rule_delete_flag=True,
            updated_time=datetime.now(),
            updated_user_name=user.user_name
        )
        await self.session.execute(delete_stmt)
        await self.session.commit()

    async def get_ooc_rule_by_id(self, ooc_rule_id: int) -> OOCRules:
        select_stmt = select(OOCRules).where(and_(OOCRules.id == ooc_rule_id, OOCRules.rule_delete_flag == False))
        result = (await self.session.execute(select_stmt)).scalars().first()
        if result is None:
            raise DatabaseError(f'ooc rule id: {ooc_rule_id} not found')
        return result

    async def get_all_ooc_rules(self) -> list[OOCRules]:
        select_stmt = select(OOCRules).where(OOCRules.rule_delete_flag == False)
        ooc_info_list: List[schemas.OOCRules] = []
        ooc_orm_list: List[general_settings.OOCRules] = (await self.session.execute(select_stmt)).scalars().all()
        for ooc_orm in ooc_orm_list:
            ooc_info_list.append(schemas.OOCRules(
                id=ooc_orm.id,
                containment_rule_id=ooc_orm.containment_rule_id,
                spec_id=ooc_orm.spec_id,
                lower_limit=ooc_orm.lower_limit,
                upper_limit=ooc_orm.upper_limit,
                create_time=ooc_orm.create_time,
                create_user_name=ooc_orm.create_user_name,
                updated_time=ooc_orm.updated_time,
                updated_user_name=ooc_orm.updated_user_name,
                rule_delete_flag=ooc_orm.rule_delete_flag
            ))
        return ooc_info_list

    async def get_ooc_rule_by_name(self, ooc_rule_name: str) -> list[OOCRules]:
        info = select(ContainmentRule.id).where(ContainmentRule.rule_name == ooc_rule_name)
        select_stmt = select(OOCRules).where(
            and_(OOCRules.containment_rule_id == info, OOCRules.rule_delete_flag == False))
        ooc_info_list: List[schemas.OOCRules] = []
        ooc_orm_list: List[general_settings.OOCRules] = (await self.session.execute(select_stmt)).scalars().all()
        for ooc_orm in ooc_orm_list:
            ooc_info_list.append(schemas.OOCRules(
                id=ooc_orm.id,
                containment_rule_id=ooc_orm.containment_rule_id,
                spec_id=ooc_orm.spec_id,
                lower_limit=ooc_orm.lower_limit,
                upper_limit=ooc_orm.upper_limit,
                create_time=ooc_orm.create_time,
                create_user_name=ooc_orm.create_user_name,
                updated_time=ooc_orm.updated_time,
                updated_user_name=ooc_orm.updated_user_name,
                rule_delete_flag=ooc_orm.rule_delete_flag
            ))
        return ooc_info_list
