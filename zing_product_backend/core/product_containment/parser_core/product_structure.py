from dataclasses import dataclass
from abc import ABC, abstractmethod, abstractproperty
from typing import List
from zing_product_backend.core import common
from zing_product_backend.app_db import mes_db_query


class Product(ABC):
    def __init__(self, _id: str,  product_type: common.ProductObjectType, virtual_factory: common.VirtualFactory,
                 fetched_data: dict = None):
        self.virtual_factory = virtual_factory
        self.fetched_data = fetched_data
        self.id = _id
        self.product_type = product_type

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'


class SublotProduct(Product):
    def get_sts_data(self, column_name: str):
        if column_name in self.fetched_data:
            return self.fetched_data[column_name]
        else:
            fetched_data_dict = mes_db_query.get_sublot_sts

    def get_sublot_data(self, column_name: str):
        if column_name in self.fetched_data:
            return self.fetched_data[column_name]
        else:
            return None

    def get_lot(self) -> 'Lot':
        fetched_data_dict = self.fetched_data

    @abstractmethod
    def get_wafering_segment(self) -> 'WaferingSegment':
        pass

    @abstractmethod
    def get_growing_segment(self) -> 'GrowingSegment':
        pass

    @abstractmethod
    def get_ingot(self) -> 'Ingot':
        pass


class Sublot(SublotProduct):
    def get_lot(self) -> 'Lot':
        pass

    def get_wafering_segment(self) -> 'WaferingSegment':
        pass

    def get_growing_segment(self) -> 'GrowingSegment':
        pass

    def get_ingot(self) -> 'Ingot':
        pass


class LotLikeProduct (Product):
    # ingot lot segment
    @abstractmethod
    def get_sublot_list(self) -> List[Sublot]:
        ...


class Lot(LotLikeProduct):
    def get_sublot_list(self) -> List[Sublot]:
        pass


class WaferingSegment(LotLikeProduct):
    def get_sublot_list(self) -> List[Sublot]:
        pass


class GrowingSegment(LotLikeProduct):
    def get_sublot_list(self) -> List[Sublot]:
        pass


class Ingot(LotLikeProduct):
    def get_sublot_list(self) -> List[Sublot]:
        pass


class ProductContainment:
    def __init__(self, target_object):
        pass

    def containment_wafer(self):
        pass

    def containment_lot(self):
        for sublot in self.target_object:
            self.containment_wafer()

    def containment_block(self):
        pass

    def containment_ingot(self):
        pass