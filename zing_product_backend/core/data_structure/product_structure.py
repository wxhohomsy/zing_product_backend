from abc import ABC, abstractmethod, abstractproperty
from typing import Union, List, Set, Dict
from zing_product_backend.core import common
from zing_product_backend.app_db import mes_db_query


class Product(ABC):
    def __init__(self, _id: str, product_type: common.ProductObjectType, virtual_factory: common.VirtualFactory):
        self.id = _id
        self.product_type = product_type
        self.virtual_factory = virtual_factory

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'


class SublotProduct(Product):
    def get_mwipsltsts_data(self, attr_name: str):
        assert attr_name.lower()
        data_mapping = mes_db_query.get_sublot_sts(self.id, self.virtual_factory)


class LotProduct(Product):
    pass


class Sublot(SublotProduct):
    def __init__(self, id):
        super().__init__()
        self.id = id

