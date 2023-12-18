from dataclasses import dataclass
from abc import ABC, abstractmethod, abstractproperty


class ContainmentRule(ABC):
    pass


class Product(ABC):
    def __init__(self, _id: str, fetched_data: dict):
        self.fetched_data = fetched_data
        self.id = _id

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'


class SublotProduct (Product):
    pass



class LotProduct(Product):
    pass


class Sublot(SublotProduct):
    def __init__(self, id):
        super().__init__()
        self.id = id


class Lot(LotProduct):
    pass


class Segment(LotProduct):
    pass


class Ingot(LotProduct):
    pass


class ProductContainment:
    def __init__(self, target_object):
        pass

    def containment_wafer(self):
        pass

    def containment_lot(self):
        pass

    def containment_block(self):
        pass

    def containment_cart(self):