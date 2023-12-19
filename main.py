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


@app.get("/test/getTime")
async def get_model():
    time.sleep(3)
    return {'current_time': datetime.datetime.now()}


@app.get("/test/nothing")
async def get_model():
    return {'data': 'nothing'}


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{request.client.host} Request: {request.method} {request.url.path} - Handled in {process_time:.4f} secs")
    return response


if __name__ == "__main__":
    from zing_product_backend.app_db import mes_db_query
    from zing_product_backend.core import common
    # df = mes_db_query.get_unit_latest_spc_data_by_operation_id_tuple(
    #     'D31520G41008', ('6700', '6200'), common.VirtualFactory.L1W)
    # df.to_csv(r'p:\e00963\test.csv')
    df = mes_db_query.get_wafering_spec_by_material_and_operation(
'3T38XPR331D', ('2920', '6700', '6200'), common.VirtualFactory.L1W)
    df.to_excel(r'p:\e00963\test_3.xlsx')