from typing import TYPE_CHECKING, Callable, Dict, Union
from sqlalchemy import text
from zing_product_backend.core.product_containment.containment_constants import (ContainmentBaseRuleClass,
                                                                                 SpcSpecialSpec, SpcOosOperators,
                                                                                 SpcValueOperators)
from zing_product_backend.core import exceptions
from zing_product_backend.app_db import external_tables
from zing_product_backend.reporting import system_log
from .. import containment_mesdb_query, local_db_query, field_utils
from ...parser_core.result_structure import ContainmentResult, ContainmentStatus, ContainmentDetailData

if TYPE_CHECKING:
    from ...parser_core.containment_structure import ContainmentBaseRule, Product
    from zing_product_backend.core import common


def spc_catch_main(base_rule: 'ContainmentBaseRule', target_product: 'Product') -> ContainmentResult:
    assert base_rule.rule_class in [ContainmentBaseRuleClass.SPC_VALUE, ContainmentBaseRuleClass.SPC_OOC,
                                        ContainmentBaseRuleClass.SPC_OOC], rf"Invalid rule class: {base_rule}"


def spc_ooc_oos_main(base_rule: 'ContainmentBaseRule', target_product: 'Product') -> ContainmentResult:
    assert base_rule.rule_class in [ContainmentBaseRuleClass.SPC_OOC, ContainmentBaseRuleClass.SPC_OOS],\
        rf"Invalid rule class: {base_rule}"
    field = base_rule.rule_data['field']\








