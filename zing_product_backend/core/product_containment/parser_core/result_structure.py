from typing import List, Tuple, Dict, Union, Optional, TYPE_CHECKING
from zing_product_backend.core.product_containment.containment_constants import *
if TYPE_CHECKING:
    from zing_product_backend.models.containment_model import ContainmentBaseRule, ContainmentRule


__all__ = [
    'ContainmentResult',
]


class ContainmentResult:
    def __init__(self, result_status: ContainmentStatus, dealt_base_rule_data_list: List['ContainmentBaseRule']):
        self.dealt_base_rule_data_list = dealt_base_rule_data_list
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
