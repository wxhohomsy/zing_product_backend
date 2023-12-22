from typing import Union
from fastapi import APIRouter
from zing_product_backend.core.common import GENERAL_RESPONSE, ResponseModel, ErrorMessages
from zing_product_backend.services.containment_rules import schemas

product_settings_router = APIRouter()


class TableColumnsResponse(ResponseModel):
    data: Union[schemas.MatInfoByGroupType, None]

