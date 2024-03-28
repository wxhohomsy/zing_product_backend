import datetime
import time
from typing import List, Union, Optional, Dict, Any, Sequence, Literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import lazyload, selectinload
from zing_product_backend.core import common, exceptions
from zing_product_backend.core.product_containment.parser_core.json_parse import extract_field_names_set
from zing_product_backend.models import containment_model, auth_model
from . import schemas, utils


def change_rule_orm_to_schema(rule_orm: containment_model.ContainmentRule) -> schemas.ContainmentRuleInfo:
    return schemas.ContainmentRuleInfo(
        id=rule_orm.id,
        rule_name=rule_orm.rule_name,
        rule_data=rule_orm.rule_data,
        changeable=rule_orm.changeable,
        created_by=rule_orm.created_by,
        created_time=rule_orm.created_time,
        updated_by=rule_orm.updated_by,
        updated_time=rule_orm.updated_time,
        created_user_name=rule_orm.created_user.user_name,
        updated_user_name=rule_orm.updated_user.user_name,
        rule_description=rule_orm.rule_description,
        containment_object_type=rule_orm.containment_object_type,
    )


def change_base_rule_orm_to_schema(rule_orm: containment_model.ContainmentBaseRule) -> schemas.ContainmentBaseRuleInfo:
    return schemas.ContainmentBaseRuleInfo(
        id=rule_orm.id,
        rule_name=rule_orm.rule_name,
        rule_class=rule_orm.rule_class,
        rule_data=rule_orm.rule_data,
        rule_sql=rule_orm.rule_sql,
        containment_object_type=rule_orm.containment_object_type,
        changeable=rule_orm.changeable,
        created_by=rule_orm.created_by,
        created_time=rule_orm.created_time,
        updated_by=rule_orm.updated_by,
        updated_time=rule_orm.updated_time,
        created_user_name=rule_orm.created_user.user_name,
        updated_user_name=rule_orm.updated_user.user_name,
        affected_rule_id_list=[rule.id for rule in rule_orm.rules],
        affected_rule_info_list=[change_rule_orm_to_schema(rule) for rule in rule_orm.rules],
        virtual_factory=rule_orm.virtual_factory,
        description=rule_orm.description,
    )


class ContainmentRuleDataBase:
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def get_all_base_rule_info(self) -> Sequence[schemas.ContainmentBaseRuleInfo]:
        """
        Get all base rules information
        :return: a list of ContainmentBaseRuleInfo
        """
        stmt = select(containment_model.ContainmentBaseRule)
        stmt = stmt.options(selectinload('*'))
        stmt = stmt.order_by(
            containment_model.ContainmentBaseRule.updated_time
        )
        base_rule_orm_list: Sequence[containment_model.ContainmentBaseRule] = (
            await self.session.execute(stmt)).scalars().all()

        base_rule_info_list = []
        for base_rule_orm in base_rule_orm_list:
            base_rule_info = change_base_rule_orm_to_schema(base_rule_orm)
            base_rule_info_list.append(base_rule_info)
        return base_rule_info_list

    async def get_all_base_rule_name(self) -> Sequence[str]:
        """
        Get all base rule names
        :return: a list of base rule names
        """
        stmt = select(containment_model.ContainmentBaseRule.rule_name)
        stmt = stmt.order_by(
            containment_model.ContainmentBaseRule.updated_time
        )
        base_rule_name_list: Sequence[str] = (await self.session.execute(stmt)).scalars().all()
        return base_rule_name_list

    async def insert_base_rule(self, base_rule_info: schemas.InsertContainmentBaseRule,
                               user: auth_model.User) -> schemas.ContainmentBaseRuleInfo:
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
            containment_object_type=base_rule_info.containment_object_type,
            description=base_rule_info.description,
        )
        self.session.add(new_base_rule)
        await self.session.commit()
        await self.session.refresh(new_base_rule)
        return change_base_rule_orm_to_schema(new_base_rule)

    async def update_base_rule(self,
                               base_rule_info: schemas.UpdateContainmentBaseRuleInfo, user: auth_model.User
                               ) -> schemas.ContainmentBaseRuleInfo:
        exist_rule = await self.session.get(containment_model.ContainmentBaseRule, base_rule_info.id)
        if exist_rule is None:
            raise exceptions.NotFoundError(rf"not found rule id: {base_rule_info.id} for update")
        else:
            if exist_rule.created_by == user.id or (exist_rule.changeable and
                                                    utils.check_containment_setting_privilege(user)):
                # every user has the permission to update the rule created by himself
                pass
            else:
                # only the user who created the rule can update the rule
                raise exceptions.InsufficientPrivilegeError(rf"Insufficient privilege to update"
                rf"rule id: {base_rule_info.id}")

            exist_rule.rule_name = base_rule_info.rule_name
            exist_rule.virtual_factory = base_rule_info.virtual_factory
            exist_rule.rule_data = base_rule_info.rule_data
            exist_rule.rule_sql = base_rule_info.rule_sql
            exist_rule.changeable = base_rule_info.changeable
            exist_rule.updated_by = user.id
            exist_rule.containment_object_type = base_rule_info.containment_object_type
            exist_rule.description = base_rule_info.description

            await self.session.commit()
            await self.session.refresh(exist_rule)
            return change_base_rule_orm_to_schema(exist_rule)

    async def delete_base_rule(self, base_rule_id: int, user: auth_model.User) -> schemas.ContainmentBaseRuleInfo:
        exist_rule = await self.session.get(containment_model.ContainmentBaseRule, base_rule_id)
        if exist_rule is None:
            raise exceptions.NotFoundError(rf"not found rule id: {base_rule_id} for delete")
        else:
            if exist_rule.updated_by == user.id:
                # every user has the permission to update the rule created by himself
                pass
            else:
                # only the user who created the rule can update the rule
                if utils.check_containment_setting_privilege(user) is False:
                    raise exceptions.InsufficientPrivilegeError(rf"Insufficient privilege to update"
                    rf"rule id: {base_rule_id}")

            await self.session.delete(exist_rule)
            await self.session.commit()
            return change_base_rule_orm_to_schema(exist_rule)

    async def get_all_rule_info(self) -> List[schemas.ContainmentRuleInfo]:
        stmt = select(containment_model.ContainmentRule)
        stmt = stmt.options(selectinload("*"))
        stmt = stmt.order_by(
            containment_model.ContainmentRule.updated_time
        )
        rule_orm_list: [containment_model.ContainmentRule] = (await self.session.execute(stmt)).scalars().all()

        rule_info_list = []
        for rule_orm in rule_orm_list:
            # Convert each ORM model instance into a schema instance
            rule_info = change_rule_orm_to_schema(rule_orm)
            rule_info_list.append(rule_info)
        return rule_info_list

    async def insert_rule_info(self, insert_rule_data: schemas.InsertContainmentRule, usr: auth_model.User
                               ) -> schemas.ContainmentRuleInfo:
        affect_base_rule_name_set = extract_field_names_set(insert_rule_data.rule_data)

        # prevent duplicate rule name
        exist_orm_stmt = select(containment_model.ContainmentRule).filter(
            containment_model.ContainmentRule.rule_name == insert_rule_data.rule_name)
        exist_orm = (await self.session.execute(exist_orm_stmt)).scalars().one_or_none()
        if exist_orm:
            raise exceptions.DuplicateError(fr'rule name: {insert_rule_data.rule_name} already exists')

        base_rule_objects = (await self.session.execute(select(containment_model.ContainmentBaseRule).filter(
            containment_model.ContainmentBaseRule.rule_name.in_(affect_base_rule_name_set)
        ))).scalars().all()

        new_rule = containment_model.ContainmentRule(
            rule_name=insert_rule_data.rule_name,
            rule_data=insert_rule_data.rule_data,
            changeable=insert_rule_data.changeable,
            created_by=usr.id,
            updated_by=usr.id,
            base_rules=list(base_rule_objects),
            rule_description=insert_rule_data.rule_description,
            containment_object_type=insert_rule_data.containment_object_type,
        )
        for base_rule in base_rule_objects:
            base_rule.rules.append(new_rule)
            await self.session.merge(base_rule)

        self.session.add(new_rule)
        await self.session.commit()
        await self.session.refresh(new_rule)
        return change_base_rule_orm_to_schema(new_rule)

    async def update_rule_info(self, update_rule_data: schemas.UpdateContainmentRule, usr: auth_model.User):
        exist_rule = await self.session.get(containment_model.ContainmentRule, update_rule_data.id)
        if exist_rule is None:
            raise exceptions.NotFoundError(rf"not found rule id: {update_rule_data.id} for update")
        else:
            if exist_rule.updated_by == usr.id or (exist_rule.changeable and
                                                   utils.check_containment_setting_privilege(usr)):
                # every user has the permission to update the rule created by himself
                pass
            else:
                # only the user who created the rule can update the rule if not changeable
                raise exceptions.InsufficientPrivilegeError(rf"Insufficient privilege to update"
                rf"rule id: {update_rule_data.id}")

            exist_rule.rule_name = update_rule_data.rule_name
            exist_rule.rule_data = update_rule_data.rule_data
            exist_rule.changeable = update_rule_data.changeable
            exist_rule.rule_description = update_rule_data.rule_description
            exist_rule.containment_object_type = update_rule_data.containment_object_type

            if str(exist_rule.rule_data) == str(update_rule_data.rule_data):
                pass
            else:
                affect_base_rule_name_set = extract_field_names_set(update_rule_data.rule_data)
                base_rules = await self.session.execute(select(containment_model.ContainmentBaseRule).filter(
                    containment_model.ContainmentBaseRule.rule_name.in_(affect_base_rule_name_set)
                    ).options(selectinload('*'))
                )
                exist_rule.base_rules = base_rules
                for base_rule in base_rules:
                    base_rule.rules.append(exist_rule)
                    await self.session.merge(base_rule)

            exist_rule.updated_by = usr.id
            await self.session.commit()
            await self.session.refresh(exist_rule)

            return change_base_rule_orm_to_schema(exist_rule)

    async def delete_rule(self, rule_id: int, usr: auth_model.User) -> schemas.ContainmentRuleInfo:
        exist_rule = await self.session.get(containment_model.ContainmentRule, rule_id)
        if exist_rule is None:
            raise exceptions.NotFoundError(rf"not found rule id: {rule_id} for delete")
        else:
            if exist_rule.updated_by == usr.id:
                # every user has the permission to update the rule created by himself
                pass
            else:
                # only the user who created the rule can update the rule
                if utils.check_containment_setting_privilege(usr) is False:
                    raise exceptions.InsufficientPrivilegeError(rf"Insufficient privilege to update"
                    rf"rule id: {rule_id}")

            await self.session.delete(exist_rule)
            await self.session.commit()
            return change_base_rule_orm_to_schema(exist_rule)


