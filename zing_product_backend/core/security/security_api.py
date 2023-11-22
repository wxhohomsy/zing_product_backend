import uuid
from sqlalchemy.exc import IntegrityError
from typing import Annotated, Set, List, Union, Optional, Literal
from pydantic import BaseModel
from enum import Enum
from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
from zing_product_backend.models import auth
from zing_product_backend.app_db import AppSession, AsyncAppSession
from zing_product_backend.core.security.security_utils import get_rules_from_user
from zing_product_backend.core.security.users import current_active_user, current_admin_user

from zing_product_backend.core.security import schema, users, crud, security_utils
from zing_product_backend.core.common import GENERAL_RESPONSE, ErrorMessages, ResponseModel
from zing_product_backend.core.security.users import UserManager
privilege_router = APIRouter()
user_info_router = APIRouter()


class PrivilegeRuleResponse(ResponseModel):
    data: Optional[List[schema.PrivilegeRuleWithGroups]]


class PrivilegeGroupResponse(ResponseModel):
    data: Optional[List[schema.PrivilegeGroupWithRules]]


class UserInfoResponse(ResponseModel):
    data: schema.UserInfo


class UserInfoList(ResponseModel):
    data: List[schema.UserInfo]


class PrivilegeGroupDeleted(BaseModel):
    id: int


@privilege_router.get("/all-privilege-groups",
                      response_model=PrivilegeGroupResponse,
                      responses=GENERAL_RESPONSE,
                      response_description="Get all privilege groups",
                      )
async def get_privilege_groups(admin_user=Depends(current_admin_user)) -> PrivilegeGroupResponse:
    async with AsyncAppSession() as session:
        privilege_db = crud.PrivilegeDataBase(session)
        privilege_groups_list = await privilege_db.get_privilege_groups()
    data_list: List[schema.PrivilegeRule] = []
    for privilege_group in privilege_groups_list:
        group_rule_name_list = []
        for rule in privilege_group.privilege_rules:
            rule_info = schema.PrivilegeRuleInfo(
                rule_name=rule.rule_name,
                rule_description=rule.rule_description,
                id=rule.id,
            )
            group_rule_name_list.append(rule_info)
        data_list.append(schema.PrivilegeGroupWithRules(
            id=privilege_group.id,
            group_name=privilege_group.group_name,
            group_description=privilege_group.group_description,
            created_by=privilege_group.created_by,
            created_time=privilege_group.created_time,
            group_deleted=privilege_group.group_deleted,
            privilege_rules=group_rule_name_list
        ))
    return {"success": True, "data": data_list}


@privilege_router.get("/all-privilege-rules",
                      response_model=PrivilegeRuleResponse,
                      responses=GENERAL_RESPONSE,
                      response_description="All privilege rules",
                      )
async def get_privilege_rules(admin_user=Depends(current_admin_user)) -> PrivilegeRuleResponse:
    async with AsyncAppSession() as session:
        privilege_db = crud.PrivilegeDataBase(session)
        privilege_rules_list = await privilege_db.get_privilege_rules()
    data_list: List[schema.PrivilegeRule] = []
    for privilege_rule in privilege_rules_list:
        rule_group_name_list = []
        for group in privilege_rule.privilege_groups:
            group_info = schema.PrivilegeGroupInfo(
                group_name=group.group_name,
                group_description=group.group_description,
                id=group.id,
            )
            rule_group_name_list.append(group_info)
        data_list.append(schema.PrivilegeRuleWithGroups(
            id=privilege_rule.id,
            rule_name=privilege_rule.rule_name,
            rule_description=privilege_rule.rule_description,
            rule_active=privilege_rule.is_active,
            privilege_groups=rule_group_name_list
        ))
    return {"success": True, "data": data_list}


@privilege_router.post("/create-privilege-groups",
                       response_model=PrivilegeGroupResponse,
                       response_description="Get all privilege groups of a user",
                       status_code=status.HTTP_200_OK,
                       summary='get all privilege groups of a user/me',
                       )
async def create_privilege_groups(privilege_group: schema.PrivilegeGroupCreate,
                                    admin_user=Depends(current_admin_user)) -> (
        PrivilegeRuleResponse):
    async with AsyncAppSession() as session:
        privilege_db = crud.PrivilegeDataBase(session)
        try:
            data = await privilege_db.create_privilege_group(privilege_group, admin_user)
        except crud.DuplicateError:
            return {"success": False, "data": None, "error_message": ErrorMessages.DUPLICATE_DATA}

    return {"success": True, "data": [
        schema.PrivilegeGroupWithRules(
            id=data.id,
            group_name=data.group_name,
            group_description=data.group_description,
            created_by=data.created_by,
            created_time=data.created_time,
            group_deleted=data.group_deleted,
            privilege_rules=[]
        )
    ],
            'success_message': 'create privilege group successfully'}


@privilege_router.post("/assign_privilege_group",
                       response_model=PrivilegeGroupResponse,
                       responses=GENERAL_RESPONSE)
async def assign_privilege_group(group_assign: schema.PrivilegeGroupAssign, admin_user=Depends(current_admin_user)):
    async with AsyncAppSession() as session:
        privilege_db = crud.PrivilegeDataBase(session)
        try:
            user_orm = await privilege_db.assign_privilege_group(group_assign)
        except crud.NotFoundError as e:
            return {"success": False, "data": None, "error_message": ErrorMessages.DATA_NOT_FOUND, "detail": str(e)}
    return {"success": True, "data": [],
            'success_message': 'assign privilege group successfully'}


@privilege_router.post("/assign_privilege_rule", response_model=PrivilegeRuleResponse,
                       responses=GENERAL_RESPONSE)
async def assign_privilege_rule(rule_assign: schema.PrivilegeRuleAssign, admin_user=Depends(current_admin_user)):
    async with AsyncAppSession() as session:
        privilege_db = crud.PrivilegeDataBase(session)
        try:
            group_orm = await privilege_db.assign_privilege_rule(rule_assign)
        except crud.NotFoundError as e:
            return {"success": False, "data": None, "error_message": ErrorMessages.DATA_NOT_FOUND, "detail": str(e)}
    return {"success": True, "data": None, "success_message": 'assign privilege rule successfully'}


@privilege_router.post("/update-privilege-rule", response_model=PrivilegeGroupResponse,
                       responses=GENERAL_RESPONSE)
async def update_privilege_rule(rule_update: schema.PrivilegeRuleUpdate, admin_user=Depends(current_admin_user)):
    async with AsyncAppSession() as session:
        privilege_db = crud.PrivilegeDataBase(session)
        try:
            group_orm = await privilege_db.update_privilege_rule(rule_update, admin_user)
        except crud.NotFoundError as e:
            return {"success": False, "data": None, "error_message": ErrorMessages.DATA_NOT_FOUND, "detail": str(e)}
    return {"success": True, "data": None, "success_message": 'update privilege rule successfully'}


@user_info_router.get("/me", response_model=UserInfoResponse, responses=GENERAL_RESPONSE)
async def me(user=Depends(current_active_user)):
    user_info = security_utils.get_user_info_from_user(user)
    return {"success": True, "data": user_info, "success_message": 'get user info successfully'}


@user_info_router.post("/me", response_model=UserInfoResponse, responses=GENERAL_RESPONSE)
async def update_me(user_info_update: schema.UserInfoUpdate, user=Depends(current_active_user)):
    async with AsyncAppSession() as session:
        privilege_db = crud.PrivilegeDataBase(session)
        user = await privilege_db.update_user_info(user, user_info_update)
        user_info = security_utils.get_user_info_from_user(user)
    return {"success": True, "data": user_info, "success_message": 'update user info successfully'}


@user_info_router.get("/all_user_info", response_model=UserInfoList, responses=GENERAL_RESPONSE)
async def all_user_info(user=Depends(current_admin_user)):
    user_info_list = []

    async with AsyncAppSession() as session:
        privilege_db = crud.PrivilegeDataBase(session)
        all_users = await privilege_db.get_all_user()
        for user in all_users:
            exist_rule_id_set = set()
            privilege_group_info_list: List[schema.PrivilegeGroupInfo] = []
            privilege_rule_info_list: List[schema.PrivilegeRuleInfo] = []

            for privilege_group in user.privilege_groups:
                if privilege_group.group_deleted:
                    continue
                privilege_group_info_list.append(schema.PrivilegeGroupInfo(
                    group_name=privilege_group.group_name,
                    group_description=privilege_group.group_description,
                    id=privilege_group.id,
                ))
                for privilege_rule in privilege_group.privilege_rules:
                    if not privilege_rule.is_active:
                        continue

                    if privilege_rule.id in exist_rule_id_set:
                        continue

                    privilege_rule_info_list.append(schema.PrivilegeRuleInfo(
                        rule_name=privilege_rule.rule_name,
                        rule_description=privilege_rule.rule_description,
                        id=privilege_rule.id,
                    ))
                    exist_rule_id_set.add(privilege_rule.id)
            user_info = schema.UserInfo(
                id=user.id,
                user_name=user.user_name,
                email=user.email,
                is_active=user.is_active,
                privilege_groups=privilege_group_info_list,
                privilege_rules=privilege_rule_info_list,
            )
            user_info_list.append(user_info)

    return {"success": True, "data": user_info_list, "success_message": 'get all users info successfully'}


