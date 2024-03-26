import typing
from zing_product_backend.core.product_containment.containment_constants import ContainmentBaseRuleClass
from zing_product_backend.core.common import ProductObjectType
from zing_product_backend.models.containment_model import ContainmentRule as ContainmentRuleModel
from typing import Callable, Dict
from ..parser_core.containment_structure import ContainmentBaseRule, ContainmentRule
from ..crud import get_containment_rule_from_rule_id

if typing.TYPE_CHECKING:
    from ..parser_core.result_structure import ContainmentResult
    from ..parser_core.containment_structure import Product


def containment_rule_parse_main(containment_rule: ContainmentRule, target_product: 'Product') -> 'ContainmentResult':
    ...


def containment_rule_parse_by_containment_id(containment_id: int, target_product: 'Product') -> 'ContainmentResult':
    containment_rule_orm = get_containment_rule_from_rule_id(containment_id)
    return containment_rule_parse_main(containment_rule_orm, target_product)
