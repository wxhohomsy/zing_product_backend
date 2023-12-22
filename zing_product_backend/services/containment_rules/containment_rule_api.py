from typing import Union
from fastapi import APIRouter
from zing_product_backend.core.common import GENERAL_RESPONSE, ResponseModel, ErrorMessages
from zing_product_backend.services.containment_rules import schemas

containment_rule_router = APIRouter()


class TableColumnsResponse(ResponseModel):
    data: Union[schemas.MatInfoByGroupType, None]

class TableColumnsResponse(ResponseModel):
    data: Union[schemas.MatInfoByGroupType, None]