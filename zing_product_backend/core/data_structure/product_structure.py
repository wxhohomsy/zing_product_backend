from abc import ABC, abstractmethod, abstractproperty
from zing_product_backend.core import common
from typing import Union, List, Set, Dict


class Product(ABC):
    def __init__(self, _id: str, product_type: common.ProductObjectType, virtual_factory: common.VirtualFactory):
        self.id = _id
        self.product_type = product_type

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'


class SublotProduct(Product):

    def get_mwipsltsts_data(self, attr_name: str):
        return self.fetched_data.get(attr_name, None)


class LotProduct(Product):
    pass


class Sublot(SublotProduct):
    def __init__(self, id):
        super().__init__()
        self.id = id

