from enum import Enum, auto
from pydantic import BaseModel
from typing import Union, List, Optional, Any, Dict


class VirtualFactory(str, Enum):
    L1W = 'L1W'
    L2W = 'L2W'
    ALL = 'ALL'


class RuleName(str, Enum):
    ADMIN = "admin"
    IMS_DEV = "ims_dev"
    PRODUCT_ASSIGN_VIEW = "product_assign_view"
    PRODUCT_ASSIGN_CHANGE = "product_assign_change"
    PRODUCT_SETTINGS_CHANGE = "product_settings_change"
    CONTAINMENT_RULE_SETTINGS_CHANGE = "containment_rule_settings_change"
    TP_AUTO_SAMPLE_SETTINGS_CHANGE = "tp_auto_sample_settings_change"


class ErrorMessages(str, Enum):
    INSUFFICIENT_PRIVILEGE = "Insufficient privilege"
    NOT_AUTHENTICATED = "Not authenticated"
    DATA_NOT_FOUND = "Data not found"
    OUTDATED_DATA = "Outdated data"
    DUPLICATE_DATA = "Duplicate data"
    DATABASE_ERROR = "Database error"


class ResponseModel(BaseModel):
    success: bool
    error_message: Union[ErrorMessages, None] = ''
    success_message: str = 'request success'
    data: Union[None, Any] = None
    detail: Optional[str] = None


class ContainmentBaseRuleType(str, Enum):
    SQL_TABLE = 'sql_table'
    CUSTOM_FUNCTION = 'custom_function'


class ProductObjectType(str, Enum):
    SUBLOT = 'sublot'
    LOT = 'lot'
    WAFERING_SEGMENT = 'wafering_segment'
    GROWING_SEGMENT = 'growing_segment'
    INGOT = 'ingot'


class PullerType(str, Enum):
    JS = 'js'
    NAST = 'nast'
    STECH = 'stech'


# ------------------------------ product auto allocation ---------------------------------


class ProductAllocationState(str, Enum):
    NORMAL = 'normal'
    HOLD = 'hold'
    START_ALLOCATING = 'start_allocating'
    WAIT_ALLOCATION_CONFIRM = 'waiting_allocation_confirm'


class ProductAllocationTransaction(str, Enum):
    INFO_UPDATE = 'info_update'
    HOLD = 'hold'
    RELEASE = 'release'
    ADAPT = 'adapt'
    BYPASS = 'bypass'
    ALLOCATION_CONFIRM = 'allocation_confirm'


PRODUCT_STATE_PERMIT_DICT = {
    ProductAllocationState.NORMAL: {
        ProductAllocationTransaction.HOLD, ProductAllocationTransaction.RELEASE, ProductAllocationTransaction.ADAPT,
        ProductAllocationTransaction.BYPASS, ProductAllocationTransaction.ALLOCATION_CONFIRM,
        ProductAllocationTransaction.INFO_UPDATE
    },
    ProductAllocationState.HOLD: {
        ProductAllocationTransaction.RELEASE, ProductAllocationTransaction.HOLD,
        ProductAllocationTransaction.INFO_UPDATE
    },
    ProductAllocationState.START_ALLOCATING: {
    },
    ProductAllocationState.WAIT_ALLOCATION_CONFIRM: {
        ProductAllocationTransaction.HOLD, ProductAllocationTransaction.RELEASE,
        ProductAllocationTransaction.ALLOCATION_CONFIRM,
        ProductAllocationTransaction.INFO_UPDATE
    }

}


class MatGroupType(str, Enum):
    YIELD_GROUP = 'yield_group'
    TEST_GROUP = 'test_group'


class MatBaseType(str, Enum):
    GROWING = 'growing'
    WAFERING = 'wafering'


# ---------------------------------TP AUTO ASSIGN---------------------------------


class TpSampleType(str, Enum):
    # segment_seed_tail/frequency/custom/ingot_tail/ingot_seed
    SEGMENT_SEED_TAIL = 'segment_seed_tail'
    FREQUENCY = 'frequency'
    INGOT_TAIL = 'ingot_tail'
    INGOT_SEED = 'ingot_seed'
    WAFER_DIRECT = 'wafer_direct'


class TpFrequencyType(str, Enum):
    FIX_COUNT = 'fix_count'
    FIX_INTERVAL_MM = 'fix_interval_mm'
    EVERY_n_LOT = 'every_n_lot'


# ------------------------------- RESPONSE ---------------------------------
GENERAL_RESPONSE: Dict[Union[int, str], Dict[str, Any]] = {
    403: {
        "description": "In sufficient privilege",
        "content": {
            "application/json": {
                "example": {"error_message": ErrorMessages.INSUFFICIENT_PRIVILEGE}
            }
        }
    },
    401: {
        "description": "Not authenticated",
        "content": {
            "application/json": {
                "example": {"error_message": ErrorMessages.NOT_AUTHENTICATED}
            }
        }
    },

}
