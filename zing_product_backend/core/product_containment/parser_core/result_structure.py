from typing import List, Tuple, Dict, Union, Optional, TYPE_CHECKING
from zing_product_backend.core.product_containment.containment_constants import *
from zing_product_backend.models.containment_model import ContainmentBaseRule, ContainmentRule
from .containment_structure import Product


__all__ = [
    'ContainmentResult',
]


class ContainmentDetailData:
    def __init__(self, base_rule: ContainmentBaseRule, target_object: 'Product',
                 result_status: ContainmentStatus, actual_value: Optional[Union[str, float, bool, List[str]]] = None,
                 additional_info: Optional[Dict] = None):
        self.base_rule = base_rule
        self.target_object = target_object
        self.result_status = result_status
        self.actual_value = actual_value
        self.additional_info = additional_info


class ContainmentResult:
    def __init__(self, result_status: ContainmentStatus, target_object: 'Product',
                 detail_data_list: List[ContainmentDetailData]):
        self.detail_data_list = detail_data_list
        self.target_object = target_object
        if type(result_status) is not ContainmentStatus:
            raise TypeError("result_status must be ContainmentStatus")
        else:
            self.result_status = result_status

    def invert(self):
        if self.result_status is ContainmentStatus.PASS:
            self.result_status = ContainmentStatus.CATCH
        elif self.result_status is ContainmentStatus.CATCH:
            self.result_status = ContainmentStatus.PASS
        return self
