from typing import Union, Tuple, List
from fastapi import APIRouter
from zing_product_backend.core.common import ResponseModel, ErrorMessages, GENERAL_RESPONSE
from zing_product_backend.core.product_containment import containment_constants, schemas
from zing_product_backend.core.product_containment.frontend_fields import build_field_main
from zing_product_backend.services.containment_rules import schemas
containment_rule_router = APIRouter()


class ContainmentBaseRuleClassResponse(ResponseModel):
    data: List[containment_constants.ContainmentBaseRuleClass]


class ContainmentBaseRuleClassInfoResponse(ResponseModel):
    data: schemas.ContainmentBaseRuleClassInfo


@containment_rule_router.get("/baseRuleClassNames", response_model=ContainmentBaseRuleClassResponse,
                             responses=GENERAL_RESPONSE)
async def get_containment_base_rule_class_names():
    return ContainmentBaseRuleClassResponse(data=containment_constants.ContainmentBaseRuleClass, success=True)


@containment_rule_router.post("/baseRuleClassInfo/{className}",
                              response_model=ContainmentBaseRuleClassInfoResponse, responses=GENERAL_RESPONSE)
async def get_containment_base_rule_class_info(className: containment_constants.ContainmentBaseRuleClass):
    field_list = build_field_main.generate_fields_main(className)
    if_sql = containment_constants.RULE_IS_SQL_DICT[className]
    return ContainmentBaseRuleClassInfoResponse(data=schemas.ContainmentBaseRuleClassInfo(
        is_sql=if_sql, fields=field_list), success=True)


