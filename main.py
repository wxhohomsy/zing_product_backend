import datetime
import time
from typing import AsyncGenerator, Annotated
import time
from fastapi import Depends, FastAPI, Request, HTTPException
from zing_product_backend.api.v1 import router_v1
from zing_product_backend.core import app
from enum import Enum
from zing_product_backend.models import auth
app.include_router(router_v1)


if __name__ == "__main__":
    from zing_product_backend.app_db import mes_db_query
    from zing_product_backend.core import common
    # df = mes_db_query.get_unit_latest_spc_data_by_operation_id_tuple(
    #     'D31520G41008', ('6700', '6200'), common.VirtualFactory.L1W)
    # df.to_csv(r'p:\e00963\test.csv')
#     df = mes_db_query.get_wafering_spec_by_material_and_operation(
# '3T38XPR331D', ('2920', '6700', '6200'), common.VirtualFactory.L1W)
#     df.to_excel(r'p:\e00963\test_3.xlsx')
    from zing_product_backend.models import auth, general_settings
    from sqlalchemy.orm import DeclarativeBase
    from sqlalchemy import inspect
    from sqlalchemy.orm import IdentityMap
    from zing_product_backend.app_db.external_tables import mwiplotsts_l1w
    # print(type(mwiplotsts_l1w))
    # print(issubclass(auth.PrivilegeRules, DeclarativeBase))
    for col in inspect(mwiplotsts_l1w).columns:
        print(col.name, issubclass(col.type.python_type, datetime.datetime))
