import datetime
from dateutil.parser import parse as time_parse
import traceback
import random
from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException
from zing_product_backend.app_db.connections import get_async_session
from zing_product_backend.app_db import mes_db_query
from zing_product_backend.core.security.users import current_active_user
from zing_product_backend.core.common import GENERAL_RESPONSE, ResponseModel, ErrorMessages, MatGroupType
from zing_product_backend.core import common
from zing_product_backend.models import auth_model
from zing_product_backend.app_db import AsyncAppSession, mes_db_query
from zing_product_backend.core.security import security_utils
from zing_product_backend.services.containment_rules.crud import ContainmentRuleDataBase
from zing_product_backend.reporting import system_log
from zing_product_backend.services.tp_auto_sample import crud, schemas, utils
from . import schemas
from . import crud
from . import dependents

to_auto_sample_router = APIRouter()


class LotInfoListResponse(ResponseModel):
    data: List[schemas.TpAssignLotInfo]


class TpSamplePlanOptionResponse(ResponseModel):
    data: schemas.TpSamplePlanOptions


class TpSampleRuleInfoListResponse(ResponseModel):
    data: List[schemas.TpSamplePlanInfo]


class InsertTpSamplePlanResponse(ResponseModel):
    data: int


class UpdateTpSamplePlanResponse(ResponseModel):
    data: schemas.TpSamplePlanInfo


class AvailableOperIdListResponse(ResponseModel):
    data: List[str]


@to_auto_sample_router.get("/availableOperList", response_model=AvailableOperIdListResponse,
                           responses=GENERAL_RESPONSE)
async def get_available_oper_id_list():
    # assume L2W has same oper as L1W
    oper_id_list = mes_db_query.get_available_oper_id_list('2205', '3000',
                                                           common.VirtualFactory.L2W)
    return AvailableOperIdListResponse(data=oper_id_list,
                                       success=True,)


@to_auto_sample_router.get("/tpLotInfoList/{virtual_factory}/{oper_id}", response_model=LotInfoListResponse,
                           responses=GENERAL_RESPONSE)
async def get_lot_info_list(oper_id: str, virtual_factory: common.VirtualFactory):
    # oper id can be all
    if oper_id == 'all':
        lot_sts_df = mes_db_query.get_lot_sts_by_oper_range('2205', '3000', virtual_factory)
    else:
        lot_sts_df = mes_db_query.get_lot_sts_by_oper_id(oper_id, virtual_factory)
    return_lot_info_list: List[schemas.TpAssignLotInfo] = []

    def generate_number():
        """Generate a number based on specified probabilities."""
        # Define the probabilities
        probabilities = [0.8, 0.05, 0.05, 0.05, 0.05]
        choices = [0, 1, 2, 3, 4]

        # Randomly select a number based on the defined probabilities
        number = random.choices(choices, probabilities)[0]
        return number

    for index, row in lot_sts_df.iterrows():
        lot_id = row['lot_id']
        lot_mat = row['mat_id']
        lot_flow = row['flow']
        oper_in_time = time_parse(row['oper_in_time'])
        last_tran_time = time_parse(row['last_tran_time'])
        tp_list: List[schemas.TPWaferInfo] = []
        if lot_id == 'B21280B004':
            # id: int
            # last_updated_time: datetime.datetime
            # tp_id: str
            # oper: str | None
            # picked: bool
            # pick_time: datetime.datetime
            # from_lot_id: str
            # key_1: str
            # key_2: str
            # key_3: str
            tp_list.extend([
                schemas.TPWaferInfo(
                    id=1,
                    last_updated_time=datetime.datetime.now(),
                    tp_id='B21280B004-01',
                    oper=None,
                    picked=False,
                    pick_time=None,
                    from_lot_id='B21280B004',
                    key_1='P+',
                    key_2='P+',
                    key_3='HC',
                ),
                schemas.TPWaferInfo(
                    id=2,
                    last_updated_time=datetime.datetime.now(),
                    tp_id='B21280B004-01',
                    oper='3100',
                    picked=True,
                    pick_time=datetime.datetime.now(),
                    from_lot_id='B21280B004',
                    key_1='POL',
                    key_2='POL',
                    key_3='HC',
                ),
                schemas.TPWaferInfo(
                    id=5,
                    last_updated_time=datetime.datetime.now(),
                    tp_id='B21280B004-01',
                    oper=None,
                    picked=False,
                    pick_time=None,
                    from_lot_id='B21280B004',
                    key_1='BF',
                    key_2='BF',
                    key_3='HC',
                ),
            ])
            to_sample_wafer_count = 2
        else:
            to_sample_wafer_count = generate_number()

        lot_info = schemas.TpAssignLotInfo(
            lot_id=lot_id,
            oper=oper_id,
            mat_id=lot_mat,
            flow=lot_flow,
            last_updated_time=datetime.datetime.now(),
            oper_in_time=oper_in_time,
            last_tran_time=last_tran_time,
            tp_list=tp_list,
            to_sample_tp_count=to_sample_wafer_count,
            virtual_factory=virtual_factory,
        )
        return_lot_info_list.append(lot_info)
    return LotInfoListResponse(data=return_lot_info_list,
                               success=True,
                               )


@to_auto_sample_router.get("/samplePlan/options", response_model=TpSamplePlanOptionResponse,
                            responses=GENERAL_RESPONSE)
async def get_sample_plan_options():
    key_options_dict = mes_db_query.get_tp_key_info()
    sample_type_list: List[common.TpSampleType] = []
    frequency_type_list: List[common.TpFrequencyType] = []
    for sample_type in common.TpSampleType:
        sample_type_list.append(sample_type)
    for frequency_type in common.TpFrequencyType:
        frequency_type_list.append(frequency_type)
    async for s in get_async_session():
        containment_rule_db = ContainmentRuleDataBase(s)
        containment_rule_list = await containment_rule_db.get_all_rule_info()
    return TpSamplePlanOptionResponse(data=schemas.TpSamplePlanOptions(
        key_1=key_options_dict['key_1'],
        key_2=key_options_dict['key_2'],
        key_3=key_options_dict['key_3'],
        sample_type=sample_type_list,
        frequency_type=frequency_type_list,
        containment_rules=containment_rule_list,
    ),
    success=True
    )


@to_auto_sample_router.get("/samplePlan/allInfo", response_model=TpSampleRuleInfoListResponse,
                            responses=GENERAL_RESPONSE)
async def get_all_sample_rule_info():
    async for s in get_async_session():
        db = crud.TPautoSampleDataBase(s)
        sample_rule_info_list = await db.get_all_sample_plan_info()
        return TpSampleRuleInfoListResponse(data=sample_rule_info_list,
                                            success=True,
                                            )


@to_auto_sample_router.post("/sampleRule/insert", response_model=InsertTpSamplePlanResponse,
                                responses=GENERAL_RESPONSE)
async def insert_sample_rule(insert_info: schemas.InsertTpSamplePlan,
                                 request_user=Depends(dependents.current_tp_sample_setting_change_user)):
    async for s in get_async_session():
        db = crud.TPautoSampleDataBase(s)
        db_id = await db.insert_sample_plan(insert_info, request_user)
        return InsertTpSamplePlanResponse(data=db_id,
                                          success=True,
                                          )


@to_auto_sample_router.post("/sampleRule/update", response_model=UpdateTpSamplePlanResponse,
                                responses=GENERAL_RESPONSE)
async def update_sample_rule(update_info: schemas.UpdateTpSampleRuleInfo,
                                 request_user=Depends(dependents.current_tp_sample_setting_change_user)):
    async for s in get_async_session():
        db = crud.TPautoSampleDataBase(s)
        sample_plan = await db.update_sample_plan(update_info, request_user)
        return UpdateTpSamplePlanResponse(data=sample_plan,
                                          success=True,
                                          )