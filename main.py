from typing import AsyncGenerator, Annotated
import time
from fastapi import Depends, FastAPI, Request, HTTPException
from zing_product_backend.api.v1 import router_v1
from zing_product_backend.core import app
from enum import Enum
from zing_product_backend.models import auth
app.include_router(router_v1)


@app.get("/")
async def hello():
    return {"message": "Hello World"}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}


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