import typing
from typing import Union, Tuple, List
from fastapi import APIRouter, Depends
from zing_product_backend.reporting import system_log
from zing_product_backend.models import auth_model
from zing_product_backend.core.security.users import current_active_user
from zing_product_backend.core.security.schema import UserInfo
from zing_product_backend.app_db.connections import get_async_session
from zing_product_backend.core.common import ResponseModel, ErrorMessages, GENERAL_RESPONSE, VirtualFactory
from zing_product_backend.core.product_containment import containment_constants, schemas
from zing_product_backend.core.product_containment.frontend_fields import build_field_main, fields_schema
from zing_product_backend.services.containment_rules import schemas
from zing_product_backend.app_db import mes_db_query
from zing_product_backend.core import common
from . import crud


containment_rule_router = APIRouter()


class ContainmentBaseRuleObjectType(ResponseModel):
    data: List[containment_constants.ProductObjectType]


class ContainmentBaseRuleClassResponse(ResponseModel):
    data: List[containment_constants.ContainmentBaseRuleClass]


class ContainmentBaseRuleClassInfoResponse(ResponseModel):
    data: schemas.ContainmentBaseRuleClassInfo


class AllContainmentBaseRuleInfoResponse(ResponseModel):
    data: List[schemas.ContainmentBaseRuleInfo]


class AllContainmentRuleInfoResponse(ResponseModel):
    data: List[schemas.ContainmentRuleInfo]


class InsertContainmentBaseRuleResponse(ResponseModel):
    data: schemas.ContainmentBaseRuleInfo


class UpdateContainmentBaseRuleResponse(ResponseModel):
    data: schemas.ContainmentBaseRuleInfo


class DeleteContainmentBaseRuleResponse(ResponseModel):
    data: schemas.ContainmentBaseRuleInfo


# containment rule response
class ContainmentRuleFieldsResponse(ResponseModel):
    data: List[schemas.fields_schema.Field]


class InsertContainmentRuleResponse(ResponseModel):
    data: schemas.ContainmentRuleInfo


class UpdateContainmentRuleResponse(ResponseModel):
    data: schemas.ContainmentRuleInfo


class DeleteContainmentRuleResponse(ResponseModel):
    data: schemas.ContainmentRuleInfo


class AvailableOperIdListResponse(ResponseModel):
    data: List[str]


@containment_rule_router.get("/containmentObjectType", response_model=ContainmentBaseRuleObjectType,
                             responses=GENERAL_RESPONSE)
async def get_containment_base_rule_class_names():
    object_list = []
    for object_type in containment_constants.ProductObjectType:
        object_list.append(object_type)
    return ContainmentBaseRuleObjectType(data=object_list, success=True)


@containment_rule_router.get("/baseRuleClassNames", response_model=ContainmentBaseRuleClassResponse,
                             responses=GENERAL_RESPONSE)
async def get_containment_base_rule_class_names():
    return ContainmentBaseRuleClassResponse(data=containment_constants.ContainmentBaseRuleClass, success=True)


@containment_rule_router.post("/baseRuleClassInfo/{className}/{virtual_factory}",
                              response_model=ContainmentBaseRuleClassInfoResponse, responses=GENERAL_RESPONSE)
async def get_containment_base_rule_class_info(className: containment_constants.ContainmentBaseRuleClass,
                                               virtual_factory: VirtualFactory):
    field_list = await build_field_main.generate_base_rule_fields_main(className, virtual_factory)
    is_sql = containment_constants.RULE_IS_SQL_DICT[className]
    is_spc = containment_constants.RULE_IS_SPC_DICT[className]
    available_object_type = containment_constants.RULE_AVAILABLE_OBJECT_TYPE[className]
    return ContainmentBaseRuleClassInfoResponse(data=schemas.ContainmentBaseRuleClassInfo(
        is_sql=is_sql, is_spc=is_spc, available_object_type=available_object_type,
        fields=field_list), success=True)


@containment_rule_router.get("/availableCharId/{oper_id}/{virtual_factory}",
                             responses=GENERAL_RESPONSE)
async def get_available_char_id(oper_id: str,
                                               virtual_factory: VirtualFactory):
    char_id_list = []
    for special_char in containment_constants.SpcSpecialSpec:
        char_id_list.append(special_char.value)
    char_id_list.extend(mes_db_query.get_spec_id_list_by_oper_id(oper_id, virtual_factory))
    # print(oper_id,virtual_factory, char_id_list)
    return ResponseModel(data=char_id_list, success=True)


@containment_rule_router.get("/containmentBaseRule/allInfo", response_model=AllContainmentBaseRuleInfoResponse,
                             responses=GENERAL_RESPONSE)
async def get_all_base_containment_rule_info():
    async for s in get_async_session():
        containment_db = crud.ContainmentRuleDataBase(s)
        sql_result = await containment_db.get_all_base_rule_info()

        return AllContainmentBaseRuleInfoResponse(data=sql_result, success=True)


@containment_rule_router.post("/containmentBaseRule/insertBaseRule",
                              response_model=InsertContainmentBaseRuleResponse,
                              responses=GENERAL_RESPONSE)
async def insert_containment_base_rule(insert_info: schemas.InsertContainmentBaseRule,
                                       usr: UserInfo = Depends(current_active_user)):
    async for s in get_async_session():
        containment_db = crud.ContainmentRuleDataBase(s)
        sql_result = await containment_db.insert_base_rule(insert_info, user=usr)
        return InsertContainmentBaseRuleResponse(data=sql_result, success=True)


@containment_rule_router.post("/containmentBaseRule/updateBaseRule",
                              response_model=UpdateContainmentBaseRuleResponse,
                              responses=GENERAL_RESPONSE)
async def update_containment_base_rule(update_info: schemas.UpdateContainmentBaseRuleInfo,
                                       usr: auth_model.User = Depends(current_active_user)):
    async for s in get_async_session():
        containment_db = crud.ContainmentRuleDataBase(s)
        sql_result = await containment_db.update_base_rule(update_info, user=usr)
        return UpdateContainmentBaseRuleResponse(data=sql_result, success=True)


@containment_rule_router.post("/containmentBaseRule/deleteBaseRule",)
async def delete_containment_base_rule( delete_base_rule: schemas.DeleteContainmentBaseRule,
                                       usr: auth_model.User = Depends(current_active_user)):
    async for s in get_async_session():
        containment_db = crud.ContainmentRuleDataBase(s)
        sql_result = await containment_db.delete_base_rule(delete_base_rule.id, user=usr)
        return DeleteContainmentBaseRuleResponse(data=sql_result, success=True)


# --------------------------------------- containment rule below ----------------------------------------------
@containment_rule_router.post("/containmentRule/insertRule", response_model=InsertContainmentRuleResponse,
                              responses=GENERAL_RESPONSE)
async def insert_containment_rule(insert_info: schemas.InsertContainmentRule,
                                  usr: auth_model.User = Depends(current_active_user)):
    async for s in get_async_session():
        containment_db = crud.ContainmentRuleDataBase(s)
        result = await containment_db.insert_rule_info(insert_info, usr=usr)
        return InsertContainmentRuleResponse(data=result, success=True, success_message="insert rule success")


@containment_rule_router.post("/containmentRule/updateRule", response_model=UpdateContainmentRuleResponse,
                              responses=GENERAL_RESPONSE)
async def update_containment_rule(update_info: schemas.UpdateContainmentRule,
                                  usr: auth_model.User = Depends(current_active_user)):
    async for s in get_async_session():
        containment_db = crud.ContainmentRuleDataBase(s)
        result = await containment_db.update_rule_info(update_info, usr=usr)
        return UpdateContainmentRuleResponse(data=result, success=True)


@containment_rule_router.get("/containmentRule/fieldInfo", response_model=ContainmentRuleFieldsResponse,
                             responses=GENERAL_RESPONSE)
async def get_containment_rule_field_info():
    async for s in get_async_session():
        containment_db = crud.ContainmentRuleDataBase(s)
        rule_name_list = await containment_db.get_all_base_rule_name()
        field_list = await build_field_main.generate_rule_fields_main(rule_name_list)
        return ContainmentRuleFieldsResponse(data=field_list,
                                             success=True)


@containment_rule_router.get("/containmentRule/allInfo", response_model=AllContainmentRuleInfoResponse,
                             responses=GENERAL_RESPONSE)
async def get_all_containment_rule_info():
    async for s in get_async_session():
        containment_db = crud.ContainmentRuleDataBase(s)
        sql_result = await containment_db.get_all_rule_info()

        return AllContainmentRuleInfoResponse(data=sql_result, success=True)


@containment_rule_router.post("/containmentRule/deleteRule", response_model=DeleteContainmentRuleResponse,
                                responses=GENERAL_RESPONSE)
async def delete_containment_rule(delete_rule: schemas.DeleteContainmentRule,
                                  usr=Depends(current_active_user)):
    async for s in get_async_session():
        containment_db = crud.ContainmentRuleDataBase(s)
        sql_result = await containment_db.delete_rule(delete_rule.id, usr=usr)
        return DeleteContainmentRuleResponse(data=sql_result, success=True, success_message='delete rule success')


@containment_rule_router.get("/containmentRule/getOper", response_model=AvailableOperIdListResponse,
                           responses=GENERAL_RESPONSE)
async def get_available_oper_id_list():
    # assume L2W has same oper as L1W
    oper_id_list = mes_db_query.get_available_oper_id_list('2100', '6898',
                                                           common.VirtualFactory.L1W)
    return AvailableOperIdListResponse(data=oper_id_list,
                                       success=True, )