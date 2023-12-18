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
    from fastapi_users import password
    a = password.PasswordHelper().hash('admin')
    a = '$2b$12$UdPtLXtM6.ictXZQ/EIhtOpDZBr8nkAwRV72EMjaGyt/EK4BXxBuW'
    print(password.PasswordHelper().verify_and_update('admin', a))