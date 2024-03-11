import traceback
from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException
from zing_product_backend.core.security.users import current_active_user
from zing_product_backend.core.security.schema import UserInfo
from zing_product_backend.core.common import GENERAL_RESPONSE, ResponseModel, ErrorMessages, MatGroupType
from zing_product_backend.core import common
from zing_product_backend.app_db import AsyncAppSession
from zing_product_backend.core.security import security_utils
from zing_product_backend.reporting import system_log
from . import schemas
from . import crud
from . import dependents
from zing_product_backend.app_db.connections import get_async_session
from zing_product_backend.services.general_settings.crud import OOCRulesCRUD

general_settings_router = APIRouter()


class MatInfoListResponse(ResponseModel):
    data: List[schemas.MatInfoByGroupType]


class MatInfoResponse(ResponseModel):
    data: Union[schemas.MatInfoByGroupType, None]


class MatGroupDetailListResponse(ResponseModel):
    data: List[schemas.MatGroupDetail]


class MatGroupDetailResponse(ResponseModel):
    data: Union[schemas.MatGroupDetail, None]


class MatGroupInfoListResponse(ResponseModel):
    data: List[schemas.MatGroupInfo]


class MatGroupInfoResponse(ResponseModel):
    data: Union[schemas.MatGroupInfo, None]


class OocInfoListResponse(ResponseModel):
    data: List[schemas.OOCRules]


class OocInfoResponse(ResponseModel):
    data: Union[schemas.OOCRules, None]


@general_settings_router.get("/matInfo/{group_type}",
                             response_model=MatInfoListResponse, responses=GENERAL_RESPONSE,
                             )
async def get_mat_info_by_group_type(group_type: MatGroupType, usr: UserInfo = Depends(current_active_user)):
    async with AsyncAppSession() as s:
        setting_database = crud.SettingsDataBase(s)
        try:
            mat_info_list = await setting_database.get_all_mat_info_restrict_by_group_type(group_type)
            return MatInfoListResponse(
                data=mat_info_list,
                success=True,
                success_message='get mat info success'
            )
        except crud.DatabaseError as e:
            system_log.server_logger.error(e)
            return MatInfoListResponse(
                data=[],
                success=False,
                success_message='error',
                detail=str(e),
                error_message=ErrorMessages.DATABASE_ERROR
            )


@general_settings_router.post("/matInfo/{group_type}",
                              response_model=MatInfoListResponse, responses=GENERAL_RESPONSE)
async def update_mat_info_restrict_with_group_type(
        group_type: MatGroupType, update_info_body: schemas.UpdateMatInfoByGroupType,
        usr: UserInfo = Depends(dependents.current_setting_change_user)):
    async with AsyncAppSession() as s:
        setting_database = crud.SettingsDataBase(s)
        try:
            await setting_database.update_mat_info(update_info_body.data, group_type, usr)
            return MatInfoListResponse(
                data=[],
                success=True,
                success_message='update mat info success'
            )
        except crud.DatabaseError as e:
            system_log.server_logger.error(traceback.format_exc())
            return MatInfoListResponse(
                data=[],
                success=False,
                success_message='error',
                detail=str(e),
                error_message=ErrorMessages.DATABASE_ERROR
            )


@general_settings_router.get("/allMatGroupDetail/{group_type}",
                             response_model=MatGroupDetailListResponse, responses=GENERAL_RESPONSE, )
async def get_all_mat_group_info(group_type: MatGroupType, usr: UserInfo = Depends(current_active_user)):
    async with AsyncAppSession() as s:
        setting_database = crud.SettingsDataBase(s)
        try:
            mat_group_list = await setting_database.get_all_mat_group_detail(group_type)
            return MatGroupDetailListResponse(
                data=mat_group_list,
                success=True,
                success_message='get mat group success'
            )
        except crud.DatabaseError as e:
            system_log.server_logger.error(traceback.format_exc())
            return MatGroupDetailListResponse(
                data=[],
                success=False,
                success_message='error',
                detail=str(e),
                error_message=ErrorMessages.DATABASE_ERROR
            )


@general_settings_router.get("/allMatGroupInfo/{group_type}",
                             response_model=MatGroupInfoListResponse, responses=GENERAL_RESPONSE, )
async def get_all_mat_group_info(group_type: MatGroupType, usr: UserInfo = Depends(current_active_user)):
    async with AsyncAppSession() as s:
        setting_database = crud.SettingsDataBase(s)
        try:
            mat_group_info_list = await setting_database.get_all_mat_group_info(group_type)
            return MatGroupInfoListResponse(
                data=mat_group_info_list,
                success=True,
                success_message='get mat group success'
            )
        except crud.DatabaseError as e:
            system_log.server_logger.error(traceback.format_exc())
            return MatGroupInfoListResponse(
                data=[],
                success=False,
                success_message='error',
                detail=str(e),
                error_message=ErrorMessages.DATABASE_ERROR
            )


@general_settings_router.get("/matGroupDetail/{group_type}/{group_id}",
                             response_model=MatGroupDetailResponse, responses=GENERAL_RESPONSE, )
async def get_mat_group_detail(group_id: int, group_type: MatGroupType,
                               usr: UserInfo = Depends(current_active_user)):
    async with AsyncAppSession() as s:
        setting_database = crud.SettingsDataBase(s)
        try:
            mat_group_detail = await setting_database.get_mat_group_detail(group_id)
            return MatGroupDetailResponse(
                data=mat_group_detail,
                success=True,
                success_message='get mat group success'
            )
        except crud.DatabaseError as e:
            system_log.server_logger.error(traceback.format_exc())
            return MatGroupDetailResponse(
                data=None,
                success=False,
                success_message='error',
                detail=str(e),
                error_message=ErrorMessages.DATABASE_ERROR
            )


@general_settings_router.get("/matInfo/{group_type}/{mat_id}",
                             response_model=MatInfoResponse, responses=GENERAL_RESPONSE, )
async def get_mat_mat_info(mat_id: int, group_type: MatGroupType,
                           usr: UserInfo = Depends(current_active_user)):
    """
    Retrieve material information based on the specified mat_id and group_type.

    :param mat_id: The ID of the material.
    :param group_type: The group type of the material.
    :param usr: The user information.
    :return: The MatInfoResponse object containing the material information.
    """
    async with AsyncAppSession() as s:
        setting_database = crud.SettingsDataBase(s)
        try:
            mat_info = await setting_database.get_mat_info_restrict_by_group_type(mat_id, group_type)
            return MatInfoResponse(
                data=mat_info,
                success=True,
                success_message='get mat info success'
            )
        except crud.DatabaseError as e:
            system_log.server_logger.error(traceback.format_exc())
            return MatInfoResponse(
                data=None,
                success=False,
                success_message='error',
                detail=str(e),
                error_message=ErrorMessages.DATABASE_ERROR
            )


@general_settings_router.post("/updateMatGroup",
                              response_model=MatGroupInfoResponse, responses=GENERAL_RESPONSE, )
async def update_mat_group(update_info_body: schemas.UpdateMatGroup,
                           usr: UserInfo = Depends(dependents.current_setting_change_user)):
    """
    Update material group.

    :param update_info_body: The body of the update request.
    :type update_info_body: schemas.UpdateMatGroup
    :param usr: The user information.
    :type usr: UserInfo
    :return: The updated mat group information response.
    :rtype: MatGroupInfoResponse
    """
    async with AsyncAppSession() as s:
        setting_database = crud.SettingsDataBase(s)
        try:
            group_info = await setting_database.update_group(to_update_group=update_info_body)
            return MatGroupInfoResponse(
                data=group_info,
                success=True,
                success_message='update mat group success'
            )
        except crud.DatabaseError as e:
            system_log.server_logger.error(traceback.format_exc())
            return MatGroupInfoResponse(
                data=None,
                success=False,
                detail=str(e),
                error_message=ErrorMessages.DATABASE_ERROR
            )


@general_settings_router.post(
    "/createMatGroup/{group_type}", response_model=MatGroupInfoResponse, responses=GENERAL_RESPONSE)
async def create_mat_group(group_type: common.MatGroupType, create_info_body: schemas.CreateMatGroup,
                           usr=Depends(dependents.current_setting_change_user)) -> MatGroupInfoResponse:
    async with AsyncAppSession() as s:
        setting_database = crud.SettingsDataBase(s)
        try:
            group_info = await setting_database.create_group(create_info_body, group_type, usr)
            return MatGroupInfoResponse(
                data=group_info,
                success=True,
                success_message='create mat group success'
            )
        except crud.DatabaseError as e:
            system_log.server_logger.error(traceback.format_exc())
            return MatGroupInfoResponse(
                data=None,
                success=False,
                detail=str(e),
                error_message=ErrorMessages.DATABASE_ERROR
            )


@general_settings_router.post("/deleteMatGroup", response_model=MatGroupInfoResponse,
                              responses=GENERAL_RESPONSE)
async def delete_mat_group(delete_info_body: schemas.DeleteMatGroup,
                           usr: UserInfo = Depends(dependents.current_setting_change_user)):
    async with AsyncAppSession() as s:
        setting_database = crud.SettingsDataBase(s)
        try:
            group_info = await setting_database.delete_group(delete_info_body)
            return MatGroupInfoResponse(
                data=group_info,
                success=True,
                success_message='delete mat group success'
            )
        except crud.DatabaseError as e:
            system_log.server_logger.error(traceback.format_exc())
            return MatGroupInfoResponse(
                data=None,
                success=False,
                detail=str(e),
                error_message=ErrorMessages.DATABASE_ERROR
            )


@general_settings_router.post("/create_ooc_rule", response_model=OocInfoResponse,  responses=GENERAL_RESPONSE)
async def create_ooc_rule(ooc_rule_data: schemas.OOCRuleCreate, user: UserInfo = Depends(current_active_user)):
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        # new_rule = await ooc_crud.create_ooc_rule(ooc_rule_data, user)
        # return new_rule
        try:
            new_rule = await ooc_crud.create_ooc_rule(ooc_rule_data, user)
            return OocInfoResponse(
                data=schemas.OOCRules.model_validate(new_rule),
                success=True,
                success_message='create ooc rule success'
            )

        except crud.DatabaseError as e:
            system_log.server_logger.error(traceback.format_exc())
            return OocInfoResponse(
                data=None,
                success=False,
                detail=str(e),
                error_message=ErrorMessages.DATABASE_ERROR
            )


@general_settings_router.post("/ooc_rule/update_rule", responses=GENERAL_RESPONSE)
async def update_rule(update_data: schemas.OOCRuleUpdate, user: UserInfo = Depends(current_active_user)):
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        await ooc_crud.update_ooc_rule(update_data, user)
        return {"message": "Rule updated"}


@general_settings_router.post("/ooc_rule/delete_rule/{ooc_rule_id}", responses=GENERAL_RESPONSE)
async def delete_rule(ooc_rule_id: int, user: UserInfo = Depends(current_active_user)):
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        await ooc_crud.delete_ooc_rule(ooc_rule_id, user)
        return {"message": "Rule deleted"}


@general_settings_router.get("/ooc_rule/get_rule_by_id/{ooc_rule_id}",response_model=OocInfoResponse, responses=GENERAL_RESPONSE)
async def get_rule_by_id(ooc_rule_id: int):
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        try:
            rule = await ooc_crud.get_ooc_rule_by_id(ooc_rule_id)
            return OocInfoResponse(
                data=schemas.OOCRules.model_validate(rule),
                success=True,
                success_message='get ooc rule success'
            )
        except crud.DatabaseError as e:
            system_log.server_logger.error(traceback.format_exc())
            return OocInfoResponse(
                data=None,
                success=False,
                detail=str(e),
                error_message=ErrorMessages.DATABASE_ERROR
            )


@general_settings_router.get("/ooc_rule/get_rule_by_name/{ooc_rule_name}", responses=GENERAL_RESPONSE)
async def get_rule_by_name(ooc_rule_name: str):
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        rule = await ooc_crud.get_ooc_rule_by_name(ooc_rule_name)
        return rule


@general_settings_router.get("/get_all_ooc_rules", responses=GENERAL_RESPONSE)
async def get_all_rules():
    async for s in get_async_session():
        ooc_crud = OOCRulesCRUD(s)
        rules = await ooc_crud.get_all_ooc_rules()
        return rules
