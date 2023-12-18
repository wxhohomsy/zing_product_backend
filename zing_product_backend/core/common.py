from enum import Enum, auto
from pydantic import BaseModel
from typing import Union, List, Optional, Any


class VirtualFactory(str, Enum):
    L1W = 'WE1'
    L2W = 'L2W'


class RuleName(str, Enum):
    ADMIN = "admin"
    IMS_DEV = "ims_dev"
    PRODUCT_ASSIGN_VIEW = "product_assign_view"
    PRODUCT_ASSIGN_CHANGE = "product_assign_change"
    PRODUCT_SETTINGS_CHANGE = "product_settings_change"


class ErrorMessages(str, Enum):
    INSUFFICIENT_PRIVILEGE = "Insufficient privilege"
    DATA_NOT_FOUND = "Data not found"
    DUPLICATE_DATA = "Duplicate data"
    DATABASE_ERROR = "Database error"


class ResponseModel(BaseModel):
    success: bool
    error_message: Union[ErrorMessages, None] = ''
    success_message: str = ''
    data: None
    detail: Optional[str] = None


class ContainmentBaseRuleType(str, Enum):
    LOT_TABLE = 'lot_sts_table'
    SUBLOT_TABLE = 'sublot_sts_table'
    CUSTOM_FUNCTION = 'custom_function'


class ContainmentCustomRuleName(str, Enum):
    DATA_OOS = 'data_oos'
    DATA_OOC = 'data_ooc'
    PULLER_ID = 'puller_id'
    CURRENT_DATETIME = 'current_datetime'
    HC_REDUCE_RULE = 'hc_reduce_rule'
    DELTA_PS_2H_MOVING_AVG = 'delta_ps_2h_moving_avg'
    DELTA_PS_2H_TO_TARGET = 'delta_ps_2h_to_target'


class ProductObjectType(str, Enum):
    SUBLOT = 'sublot'
    LOT = 'lot'
    SEGMENT = 'segment'
    INGOT = 'ingot'


class ProductStatus(str, Enum):
    NORMAL = 'NORMAL'
    HOLD = 'HOLD'
    START = 'START'



class ProductionTransaction(str, Enum):
    HOLD = 'HOLD'
    RELEASE = 'RELEASE'
    BYPASS = 'BYPASS'


class MatGroupType(str, Enum):
    YIELD_GROUP = 'yield_group'
    TEST_GROUP = 'test_group'


class MatBaseType(str, Enum):
    GROWING = 'growing'
    WAFERING = 'wafering'


# ------------------------------- RESPONSE ---------------------------------
GENERAL_RESPONSE = {
             403: {
                 "description": "Forbidden",
                 "content": {
                     "application/json": {
                         "example": {"detail": ErrorMessages.INSUFFICIENT_PRIVILEGE}
                     }
                 }
             }
         }