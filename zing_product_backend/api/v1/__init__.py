from fastapi import APIRouter
from zing_product_backend.api.v1 import auth
from zing_product_backend.services.product_settings import product_setting_api
from zing_product_backend.services.containment_rules import containment_rule_api
from zing_product_backend.services.tp_auto_sample import tp_auto_sample_api
# from zing_product_backend.services.tp_auto_sample import tp_au


router_v1 = APIRouter()
router_v1.include_router(auth.router)
router_v1.include_router(product_setting_api.product_settings_router,
                         prefix="/productSettings", tags=["product_settings"])
router_v1.include_router(containment_rule_api.containment_rule_router,
                         prefix="/containmentRules", tags=["containment_rules"])
router_v1.include_router(tp_auto_sample_api.to_auto_sample_router,
                            prefix="/tpAutoSample", tags=["tp_auto_sample"])