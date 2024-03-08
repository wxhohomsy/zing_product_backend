import typing
from typing import Union, Tuple, List
from fastapi import APIRouter, Depends
from zing_product_backend.reporting import system_log
from zing_product_backend.models import auth_model
from zing_product_backend.core.security.users import current_active_user
from zing_product_backend.core.security.schema import UserInfo
from fastapi import APIRouter, Depends
from zing_product_backend.core.security.users import current_active_user
from zing_product_backend.services.ooc_rules.crud import OOCRulesCRUD
from zing_product_backend.app_db.connections import get_async_session
from . import schemas

ooc_rules_router = APIRouter()


@ooc_rules_router.post("/creat_ooc_rule")
async def create_rule(ooc_rule_data: schemas.OOCRuleCreate, user: UserInfo = Depends(current_active_user)):
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        new_rule = await ooc_crud.create_ooc_rule(ooc_rule_data, user)
        return new_rule


@ooc_rules_router.post("/ooc_rule/update_rule")
async def update_rule(update_data: schemas.OOCRuleUpdate, user: UserInfo = Depends(current_active_user)):
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        await ooc_crud.update_ooc_rule(update_data, user)
        return {"message": "Rule updated"}


@ooc_rules_router.post("/ooc_rule/delete_rule/{ooc_rule_id}")
async def delete_rule(ooc_rule_id: int, user: UserInfo = Depends(current_active_user)):
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        await ooc_crud.delete_ooc_rule(ooc_rule_id, user)
        return {"message": "Rule deleted"}


@ooc_rules_router.get("/ooc_rule/get_rule_by_id/{ooc_rule_id}")
async def get_rule_by_id(ooc_rule_id: int):
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        rule = await ooc_crud.get_ooc_rule_by_id(ooc_rule_id)
        return rule


@ooc_rules_router.get("/ooc_rule/get_rule_by_name/{ooc_rule_name}")
async def get_rule_by_name(ooc_rule_name: str):
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        rule = await ooc_crud.get_ooc_rule_by_name(ooc_rule_name)
        return rule


@ooc_rules_router.get("/get_all_ooc_rules")
async def get_all_rules():
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        rules = await ooc_crud.get_all_ooc_rules()
        return rules
