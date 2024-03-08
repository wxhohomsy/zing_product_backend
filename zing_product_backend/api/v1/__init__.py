from fastapi import APIRouter
from zing_product_backend.api.v1 import auth
from zing_product_backend.core.security import security_api
from zing_product_backend.services.general_settings import general_setting_api
from zing_product_backend.services.containment_rules import containment_rule_api
from zing_product_backend.services.tp_auto_sample import tp_auto_sample_api
from zing_product_backend.services.product_auto_allocation import auto_allocation_api
from zing_product_backend.services.ooc_rules import ooc_rules_api


router_v1 = APIRouter()
router_v1.include_router(auth.router)

router_v1.include_router(general_setting_api.general_settings_router,
                         prefix="/generalSettings", tags=["general_settings"])
router_v1.include_router(containment_rule_api.containment_rule_router,
                         prefix="/containmentRules", tags=["containment_rules"])
router_v1.include_router(tp_auto_sample_api.to_auto_sample_router,
                            prefix="/tpAutoSample", tags=["tp_auto_sample"])
router_v1.include_router(auto_allocation_api.auto_allocation_router,
                            prefix="/autoAllocation", tags=["auto_allocation"])
router_v1.include_router(ooc_rules_api.ooc_rules_router,
                            prefix="/oocRules", tags=["ooc_rules"])
