import typing

from zing_product_backend.core.product_containment.containment_constants import ContainmentBaseRuleClass
from zing_product_backend.core.common import ProductObjectType
from typing import Callable, Dict
from .m1_fdc import m1_fdc_main
from .mesdb_table import mesdb_table_main
from .spc_catch import spc_catch_main
from .time_related import time_related_main
from .crystal_defect import crystal_defect_main
from .predefined_group import predefined_group_main

if typing.TYPE_CHECKING:
    from ..parser_core.result_structure import ContainmentResult
    from ..parser_core.containment_structure import Product


def create_parser_function(rule_name: ContainmentBaseRuleClass) -> Callable[[Dict, Product], ContainmentResult]:
    if rule_name in [ContainmentBaseRuleClass.INGOT_FDC]:
        return m1_fdc_main(rule_name)

    elif rule_name in [ContainmentBaseRuleClass.MWIPMATDEF, ContainmentBaseRuleClass.MWIPSLTSTS,
                       ContainmentBaseRuleClass.MWIPSLTSTS, ContainmentBaseRuleClass.MESDB_CUSTOM_SQL]:
        return mesdb_table_main(rule_name)

    elif rule_name in [ContainmentBaseRuleClass.SPC_VALUE, ContainmentBaseRuleClass.SPC_OOC,
                       ContainmentBaseRuleClass.SPC_OOS]:
        return spc_catch_main(rule_name)
