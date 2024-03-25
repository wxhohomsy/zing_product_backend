import os

from zing_product_backend import settings
if settings.DEBUG:
    from dotenv import load_dotenv
    load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from zing_product_backend.core import exceptions, common
from zing_product_backend.core.middlewares import request_record_middleware
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()


@app.exception_handler(exceptions.PredefinedException)
async def base_exception_handler(request: Request, exc: exceptions.PredefinedException):
    # Common handling logic
    response_model = common.ResponseModel(
        success=False,
        error_message=exc.message,
        detail=exc.detail,
        success_message='failed'
    )
    return JSONResponse(content=response_model.model_dump(), status_code=exc.code)

app.middleware("http")(request_record_middleware)
session_secret_key = os.getenv('SESSION_SECRET_KEY')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://10.9.16.19:5173", "http://10.9.16.30:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=session_secret_key, same_site='lax')


@app.middleware("http")
async def dispatch(request: Request, call_next):
    response = await call_next(request)
    # Set a cookie in the response
    return response

# Create a FastAPI application

# Optionally, create a sub-application if you want the middleware to apply only to specific routes
