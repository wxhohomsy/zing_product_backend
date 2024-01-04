from abc import ABC, abstractmethod
from zing_product_backend.core import common
from zing_product_backend.models import containment_model
from zing_product_backend.core.product_containment.containment_constants import *
from zing_product_backend.core.product_containment.parser_core import product_structure
from zing_product_backend.core.product_containment.parser_core import result_structure


class ContainmentRule:
    def __init__(self, containment_rule_orm: containment_model.ContainmentRule):
        self.containment_object_type = containment_rule_orm.containment_object_type
        self.rule_data = containment_rule_orm.rule_data


class ContainmentBaseRule(ABC):
    def __init__(self, rule_name: BaseRuleName, containment_object_type: common.ProductObjectType):
        self.rule_name = rule_name
        self.rule_input_type = RULE_INPUT_TYPE_DICT[rule_name]

    def containment_product(self, product: product_structure.Product) -> result_structure.ContainmentResult:
        if product.product_type == common.ProductObjectType.LOT:
            return self.containment_lot(product)
        elif product.product_type == common.ProductObjectType.SUBLOT:
            return self.containment_sublot(product)
        elif product.product_type == common.ProductObjectType.WAFERING_SEGMENT:
            return self.containment_wafering_segment(product)
        elif product.product_type == common.ProductObjectType.GROWING_SEGMENT:
            return self.containment_growing_segment(product)
        elif product.product_type == common.ProductObjectType.INGOT:
            return self.containment_ingot(product)

    @abstractmethod
    def containment_sublot(self, product: product_structure.Sublot) -> result_structure.ContainmentResult:
        pass

    @abstractmethod
    def containment_lot(self, product: product_structure.Lot) -> result_structure.ContainmentResult:
        pass

    @abstractmethod
    def containment_wafering_segment(self, product: product_structure.WaferingSegment) -> \
            result_structure.ContainmentResult:
        pass

    @abstractmethod
    def containment_growing_segment(self, product: product_structure.GrowingSegment) -> (
            result_structure.ContainmentResult):
        pass

    @abstractmethod
    def containment_ingot(self, product: product_structure.Ingot):
        pass

