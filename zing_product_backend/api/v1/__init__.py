from fastapi import APIRouter
from zing_product_backend.api.v1 import auth
from zing_product_backend.services.product_settings import product_setting_api

router_v1 = APIRouter()
router_v1.include_router(auth.router)
router_v1.include_router(product_setting_api.product_settings_router,
                         prefix="/product_settings", tags=["product_settings"])