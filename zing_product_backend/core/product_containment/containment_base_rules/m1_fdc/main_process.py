from typing import TYPE_CHECKING
from zing_product_backend.core.product_containment.containment_constants import ContainmentBaseRuleClass
from . import fdc_data_fetch
from ...parser_core.result_structure import ContainmentResult, ContainmentStatus, ContainmentDetailData
if TYPE_CHECKING:
    from ...parser_core.containment_structure import ContainmentBaseRule, Product, Sublot
    from zing_product_backend.core import common


def m1_fdc_main(base_rule: 'ContainmentBaseRule', target_product: 'Product') -> ContainmentResult:
    assert isinstance(target_product, Sublot), 'm1_fdc_main only accept sublot'
    wafer_position = float(target_product.get_sts_data('sublot_cmf_9')) * 10  #unit in mm
    wafer_position_index = int(wafer_position)
    ingot_data_array = fdc_data_fetch.get_ingot_fdc_data(base_rule)