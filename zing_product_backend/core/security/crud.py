import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.password import PasswordHelper
from typing import Optional, Dict, Any, Union, List
from zing_product_backend.models import auth
from zing_product_backend.reporting import system_log
from zing_product_backend.core.security import schema
from zing_product_backend.core.security import user_init
import db_init


class DuplicateError(Exception):
    pass


class NotFoundError(Exception):
    pass


class ZingUserDatabase(SQLAlchemyUserDatabase):
    user_table: type[auth.User]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.privilege_group_table = auth.PrivilegeGroup
        # print(*args)
        # print(dict(**kwargs))

    async def get_by_user_name(self, user_name: str) -> Optional[schema.User]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.user_name) == func.lower(user_name)
        )
        return await self._get_user(statement)

    async def create(self, create_dict: Dict[str, Any]) -> auth.User:
        # Create a new user
        user = self.user_table(**create_dict)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        # Check if a privilege group already exists
        group_results = await self.session.execute(select(self.privilege_group_table).limit(1))
        data = group_results.scalars().all()

        # If no group exists, create an admin group and add this user to it
        if len(data) == 0:
            admin_group = auth.PrivilegeGroup(group_name='admin', created_by=user.id, created_time=func.now())
            user.privilege_groups.append(admin_group)
            admin_rule = auth.PrivilegeRules(rule_name='admin', rule_description='admin')
            admin_group.privilege_rules.append(admin_rule)
            system_log.server_logger.info(f'init admin group for user {user.user_name}')
            await self.session.commit()
            await self.session.refresh(user)
            await user_init.create_default_user(user, self.session)
            await db_init.load_mat_info(user, self.session)
        return user


class PrivilegeDataBase:
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def get_privilege_rules(self) -> List[auth.PrivilegeRules]:
        stmt = select(auth.PrivilegeRules)
        data = await self.session.execute(stmt)
        return data.scalars().all()

    async def get_privilege_groups(self) -> list[auth.PrivilegeGroup]:
        stmt = select(auth.PrivilegeGroup)
        data = await self.session.execute(stmt)
        return data.scalars().all()

    async def get_active_privilege_group_by_name(self, group_name: str) -> auth.PrivilegeGroup:
        stmt = select(auth.PrivilegeGroup).where(and_(auth.PrivilegeGroup.group_name == group_name,
                                                      auth.PrivilegeGroup.group_deleted == False))
        data = await self.session.execute(stmt)
        return data.scalar()

    async def get_privilege_group_by_id(self, group_id: int, need_active=False) -> auth.PrivilegeGroup:
        stmt = select(auth.PrivilegeGroup).where(auth.PrivilegeGroup.id == group_id)
        if need_active is True:
            stmt = stmt.where(auth.PrivilegeGroup.group_deleted == False)
        data = await self.session.execute(stmt)
        group_orm = data.scalar()
        if group_orm is None:
            raise NotFoundError(rf'Group not found for group id {group_id}')
        await self.session.refresh(group_orm)
        return group_orm

    async def get_privilege_rule_by_id(self, rule_id: uuid.UUID, need_active=False) -> auth.PrivilegeGroup:
        stmt = select(auth.PrivilegeRules).where(auth.PrivilegeRules.id == rule_id)
        if need_active is True:
            stmt = stmt.where(auth.PrivilegeRules.rule_active == False)
        data = await self.session.execute(stmt)
        rule_orm = data.scalar()
        await self.session.refresh(rule_orm)
        return rule_orm

    async def get_user_by_user_id(self, user_id: uuid.UUID) -> Union[auth.User, None]:
        user_result = await self.session.execute(select(auth.User).where(auth.User.id == user_id))
        data = user_result.scalar()
        if data is None:
            raise NotFoundError(rf'User not found for user id {user_id}')
        else:
            await self.session.refresh(data)
            return data

    async def get_all_user(self) -> List[auth.User]:
        user_result = await self.session.execute(select(auth.User))
        data = user_result.scalars().all()
        return data

    async def create_privilege_group(self, privilege_group: schema.PrivilegeGroup,
                                     user: auth.User) -> auth.PrivilegeGroup:
        privilege_group_orm = auth.PrivilegeGroup(
            group_name=privilege_group.group_name,
            group_description=privilege_group.group_description,
            created_by=user.id,
            created_time=func.now(),
            group_deleted=False
        )
        exist_group = await self.get_active_privilege_group_by_name(privilege_group.group_name)
        if exist_group is not None:
            raise DuplicateError('Group name already exists')
        self.session.add(privilege_group_orm)
        await self.session.commit()
        await self.session.refresh(privilege_group_orm)
        return privilege_group_orm

    async def assign_privilege_group(self, privilege_group_assign: schema.PrivilegeGroupAssign) -> auth.User:
        user_id = privilege_group_assign.user_id
        user_orm = await self.get_user_by_user_id(user_id)
        if user_orm is None:
            raise NotFoundError(rf'User not found for user id {user_id}')

        group_orm_list = []
        for group_id in privilege_group_assign.group_id_list:
            group_orm = await self.get_privilege_group_by_id(group_id)
            if group_orm is None:
                raise NotFoundError(rf'Group not found for group id {group_id}')
            group_orm_list.append(group_orm)

        user_orm.privilege_groups = group_orm_list

        await self.session.commit()
        await self.session.refresh(user_orm)
        return user_orm

    async def assign_privilege_rule(self, privilege_rule_assign: schema.PrivilegeRuleAssign) -> auth.PrivilegeGroup:
        group_id = privilege_rule_assign.group_id
        group_orm = await self.get_privilege_group_by_id(group_id)
        if group_orm is None:
            raise NotFoundError('group not found')
        rule_orm_list = []
        for rule_id in privilege_rule_assign.rule_id_list:
            rule_orm = await self.get_privilege_rule_by_id(rule_id)
            if group_orm is None:
                raise NotFoundError('Group not found')
            rule_orm_list.append(rule_orm)
        group_orm.privilege_rules = rule_orm_list
        await self.session.commit()
        await self.session.refresh(group_orm)
        return group_orm

    async def create_privilege_rule(self, privilege_rule: schema.PrivilegeRuleCreate, user: auth.User) -> \
            auth.PrivilegeRules:
        privilege_rule_orm = auth.PrivilegeRules(
            rule_name=privilege_rule.rule_name,
            rule_description=privilege_rule.rule_description,
            rule_active=True,
        )
        self.session.add(privilege_rule_orm)
        await self.session.commit()
        await self.session.refresh(privilege_rule_orm)
        return privilege_rule_orm

    async def update_privilege_rule(self, privilege_rule: schema.PrivilegeRuleUpdate, user: auth.User) -> \
            auth.PrivilegeRules:
        privilege_rule_orm = await self.get_privilege_rule_by_id(privilege_rule.id)
        privilege_rule_orm.rule_name = privilege_rule.rule_name
        privilege_rule_orm.rule_description = privilege_rule.rule_description
        privilege_rule_orm.rule_active = privilege_rule.rule_active
        await self.session.commit()
        await self.session.refresh(privilege_rule_orm)
        return privilege_rule_orm

    async def update_user_info(self, user: auth.User, user_info_update: schema.UserInfoUpdate):
        user = await self.get_user_by_user_id(user.id)
        password_helper = PasswordHelper()
        if user_info_update.email is not None:
            user.email = user_info_update.email
        if user_info_update.password is not None:
            hashed_password = password_helper.hash(user_info_update.password)
            user.hashed_password = hashed_password

        await self.session.commit()
        await self.session.refresh(user)
        return user

