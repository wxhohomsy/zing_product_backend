from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from zing_product_backend.core import exceptions, common
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)