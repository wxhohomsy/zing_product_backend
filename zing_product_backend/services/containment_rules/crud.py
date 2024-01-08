import time
from typing import List, Union, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import lazyload, selectinload
from zing_product_backend.core import common, exceptions
from zing_product_backend.models import containment_model, auth
from . import schemas


class ContainmentRuleDataBase:
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def get_all_base_rule_info(self) -> List[schemas.ContainmentBaseRuleInfo]:
        """
        Get all base rules information
        :return: a list of ContainmentBaseRuleInfo
        """
        stmt = select(containment_model.ContainmentBaseRule)
        stmt = stmt.options(selectinload('*'))
        stmt = stmt.order_by(
            containment_model.ContainmentBaseRule.updated_time
        )
        base_rule_orm_list: List[containment_model.ContainmentBaseRule] = (await self.session.execute(stmt)).scalars().all()

        base_rule_info_list = []
        for base_rule_orm in base_rule_orm_list:
            affected_rule_group_id_list = [
                rule_group.id for rule_group in base_rule_orm.rules
            ]
            base_rule_info = schemas.ContainmentBaseRuleInfo(
                id=base_rule_orm.id,
                rule_class=base_rule_orm.rule_class,
                rule_data=base_rule_orm.rule_data,
                rule_sql=base_rule_orm.rule_sql,
                changeable=base_rule_orm.changeable,
                created_by=base_rule_orm.created_by,
                created_time=base_rule_orm.created_time,
                updated_by=base_rule_orm.updated_by,
                updated_time=base_rule_orm.updated_time,
                created_user_name=base_rule_orm.created_user.user_name,
                updated_user_name=base_rule_orm.updated_user.user_name,
                affected_rule_group_id_list=affected_rule_group_id_list,
                virtual_factory=base_rule_orm.virtual_factory,

                )
            base_rule_info_list.append(base_rule_info)
        return base_rule_info_list

    async def insert_base_rule(self, base_rule_info: schemas.InsertContainmentBaseRule, user: auth.User) -> int:
        """
        Insert a new base rule
        :param base_rule_info: schemas.InsertContainmentBaseRule
        :param user: auth.User
        :return: int
        """
        exist_orm = (await self.session.execute(
            select(containment_model.ContainmentBaseRule).filter(
                containment_model.ContainmentBaseRule.rule_name == base_rule_info.rule_name
            )
        )).scalar_one_or_none()

        if exist_orm is not None:
            raise exceptions.DuplicateError(rf"already exist rule name: {base_rule_info.rule_name}, id: {exist_orm.id},"
                                           rf"created by: {exist_orm.created_user.user_name}")
        new_base_rule = containment_model.ContainmentBaseRule(
            rule_class=base_rule_info.rule_class,
            rule_name=base_rule_info.rule_name,
            virtual_factory=base_rule_info.virtual_factory,
            rule_data=base_rule_info.rule_data,
            rule_sql=base_rule_info.rule_sql,
            changeable=base_rule_info.changeable,
            created_by=user.id,
            updated_by=user.id,
            containment_object_type=base_rule_info.containment_object_type
        )
        self.session.add(new_base_rule)
        await self.session.commit()
        await self.session.refresh(new_base_rule)
        return new_base_rule.id

    async def update_base_rule(self, base_rule_info: schemas.UpdateContainmentBaseRuleInfo, user: auth.User) -> int:
        exist_rule = await self.session.get(containment_model.ContainmentBaseRule, base_rule_info.id)
        if exist_rule is None:
            raise exceptions.NotFoundError(rf"not found rule id: {base_rule_info.id} for update")
        else:
            if exist_rule.updated_by == user.id:
                # every user has the permission to update the rule created by himself
                pass
            else:
                # only the user who created the rule can update the rule

                raise exceptions.PermissionError(rf"not the creator of rule id: {base_rule_info.id}")

            exist_rule.rule_class = base_rule_info.rule_class
            exist_rule.rule_name = base_rule_info.rule_name
            exist_rule.virtual_factory = base_rule_info.virtual_factory
            exist_rule.rule_data = base_rule_info.rule_data
            exist_rule.rule_sql = base_rule_info.rule_sql
            exist_rule.changeable = base_rule_info.changeable
            exist_rule.updated_by = user.id
            exist_rule.containment_object_type = base_rule_info.containment_object_type
            await self.session.commit()
            await self.session.refresh(exist_rule)
            return exist_rule.id
