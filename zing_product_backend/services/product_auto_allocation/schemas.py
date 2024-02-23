from typing import List, Union, Dict, Set, Literal
from uuid import UUID
import datetime
from pydantic import BaseModel
from zing_product_backend.core import common


class AllocationState(BaseModel):
    state_code: common.ProductAllocationState
    state_time: datetime.datetime
    state_comment: str


class LotStatus(BaseModel):
    lot_id: str
    active_states: List[AllocationState]
    transaction_id: int
    current_oper: str
    current_mat_id: str
    target_mat_id: str
    last_update_time: datetime.datetime
    last_update_user_name: str
    last_comment: str
    virtual_factory: str
    missing_chars: List[str]
    wafer_count: int



