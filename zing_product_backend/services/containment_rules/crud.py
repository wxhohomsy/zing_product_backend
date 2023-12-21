import time
from typing import List, Union, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import lazyload
from zing_product_backend.core import common
from zing_product_backend.app_db.external_tables import mwipsltsts_l1w, mwiplotsts_l1w, mwipmatdef_l1w


def get_table_column_data(table_name: common.ContainmentTableName):
    if table_name == common.ContainmentTableName.MWIPMATDEF:
        return mwipmatdef_l1w.c
    elif table_name == common.ContainmentTableName.MWIPSLTSTS:
        return mwipsltsts_l1w.c
    elif table_name == common.ContainmentTableName.MWIPLOTSTS:
        return mwiplotsts_l1w.c


class ContainmentRuleDataBase:
    def __init__(self, async_session: AsyncSession):
        self.session = async_session


