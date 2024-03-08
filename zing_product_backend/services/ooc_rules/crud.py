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
from zing_product_backend.models.containment_model import OOCRules, ContainmentRule
from datetime import datetime
from zing_product_backend.services.containment_rules import containment_rule_api
from sqlalchemy.orm import Session
from typing import List

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from zing_product_backend.core.security.schema import UserInfo


class OOCRulesCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_ooc_rule(self, ooc_rule_data: schemas.OOCRuleCreate, user: UserInfo) -> OOCRules:
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
        update_stmt = update(OOCRules).where(OOCRules.id == update_data.id).values(
            lower_limit=update_data.lower_limit,
            upper_limit=update_data.upper_limit,
            updated_time=datetime.now(),
            updated_user_name=user.user_name
        )
        await self.session.execute(update_stmt)
        await self.session.commit()

    async def delete_ooc_rule(self, ooc_rule_id: int, user: UserInfo) -> None:
        delete_stmt = update(OOCRules).where(OOCRules.id == ooc_rule_id).values(
            rule_delete_flag=True,
            updated_time=datetime.now(),
            updated_user_name=user.user_name
        )
        await self.session.execute(delete_stmt)
        await self.session.commit()

    async def get_ooc_rule_by_id(self, ooc_rule_id: int) -> OOCRules:
        info = containment_rule_api.get_all_base_containment_rule_info
        print()
        select_stmt = select(OOCRules).where(and_(OOCRules.id == ooc_rule_id, OOCRules.rule_delete_flag == False))
        result = await self.session.execute(select_stmt)
        return result.scalars().first()

    async def get_all_ooc_rules(self) -> list[OOCRules]:
        select_stmt = select(OOCRules).where(OOCRules.rule_delete_flag == False)
        result = await self.session.execute(select_stmt)
        return result.scalars().all()

    async def get_ooc_rule_by_name(self, ooc_rule_name: str) -> OOCRules:
        info = select(ContainmentRule.id).where(ContainmentRule.rule_name == ooc_rule_name)
        select_stmt = select(OOCRules).where(and_(OOCRules.containment_rule_id == info, OOCRules.rule_delete_flag == False))
        print(select_stmt)
        result = await self.session.execute(select_stmt)
        return result.scalars().first()
