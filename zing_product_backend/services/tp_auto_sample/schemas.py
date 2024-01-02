import datetime
from typing import List, Dict, Set, Literal, Union
from pydantic import BaseModel
from zing_product_backend.core import common, common_type


class TPWaferInfo(BaseModel):
    id: int
    last_updated_time: datetime.datetime
    tp_id: str
    oper: Union[str, None]
    picked: bool
    pick_time: Union[datetime.datetime, None]
    from_lot_id: str
    key_1: str
    key_2: str
    key_3: str


class TpAssignLotInfo(BaseModel):
    last_tran_time: datetime.datetime
    oper_in_time: datetime.datetime
    last_updated_time: datetime.datetime
    lot_id: str
    mat_id: str
    flow: str
    oper: str
    tp_list: list[TPWaferInfo]
    to_sample_tp_count: int
    virtual_factory: common.VirtualFactory



