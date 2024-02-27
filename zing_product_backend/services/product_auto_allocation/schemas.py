from typing import List, Union, Dict, Set, Literal
from uuid import UUID
import datetime
from pydantic import BaseModel
from zing_product_backend.core import common


class AllocationState(BaseModel):
    state_code: common.ProductAllocationState
    state_time: datetime.datetime
    state_comment: str
    id: int


class LotStatus(BaseModel):
    lot_id: str
    active_states: List[AllocationState]
    current_transaction_seq: int
    current_oper: str
    current_mat_id: str
    target_mat_id: str
    last_updated_time: datetime.datetime
    last_updated_user_name: str
    last_comment: str
    virtual_factory: str
    missing_chars: List[str]
    wafer_count: int


class LotTransaction(BaseModel):
    lot_id: str
    transaction_seq: int
    transaction_code: common.ProductAllocationTransaction
    comment: str
    transaction_time: datetime.datetime
    state_code_list: List[AllocationState]
    oper: str
    mat_id: str
    target_mat_id: str
    missing_char: str


class HoldLot(LotTransaction):
    pass


class ReleaseLot(LotTransaction):
    hold_id: int
