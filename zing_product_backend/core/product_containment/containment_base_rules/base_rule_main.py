import typing

from zing_product_backend.core.product_containment.containment_constants import ContainmentBaseRuleClass
from zing_product_backend.core.common import ProductObjectType
from typing import Callable, Dict
from .m1_fdc import m1_fdc_main
from .mesdb_table import mesdb_table_main
from .spc_catch import spc_catch_main
from .time_related import time_related_main
from .crystal_defect import crystal_defect_main
from .mat_group import mat_group_main
from ..parser_core.containment_structure import ContainmentBaseRule
if typing.TYPE_CHECKING:
    from ..parser_core.result_structure import ContainmentResult
    from ..parser_core.containment_structure import Product


def parse_main(containment_base_rule: ContainmentBaseRule, target_product: 'Product') -> 'ContainmentResult':
    rule_name = containment_base_rule.rule_name
    if rule_name in [ContainmentBaseRuleClass.INGOT_FDC]:
        return m1_fdc_main(containment_base_rule, target_product)

    elif rule_name in [ContainmentBaseRuleClass.MWIPMATDEF, ContainmentBaseRuleClass.MWIPSLTSTS,
                       ContainmentBaseRuleClass.MWIPSLTSTS, ContainmentBaseRuleClass.MESDB_CUSTOM_SQL]:
        return mesdb_table_main(containment_base_rule, target_product)

    elif rule_name in [ContainmentBaseRuleClass.MAT_GROUP]:
        return mat_group_main(containment_base_rule, target_product)

    elif rule_name in [ContainmentBaseRuleClass.SPC_VALUE, ContainmentBaseRuleClass.SPC_OOC,
                       ContainmentBaseRuleClass.SPC_OOS]:
        return spc_catch_main(containment_base_rule, target_product)