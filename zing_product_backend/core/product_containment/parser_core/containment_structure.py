import functools
from dataclasses import dataclass
import pydantic
from abc import ABC, abstractmethod, abstractproperty
from typing import List, Dict
from functools import cached_property
from zing_product_backend.global_utils import function_utils
from zing_product_backend.core import common
from zing_product_backend.app_db import mes_db_query
from zing_product_backend.models import containment_model
from . import result_structure


class Product:
    def __init__(self, _id: str, virtual_factory: common.VirtualFactory,
                 fetched_data: dict = None):
        self.fetched_data = fetched_data
        self.id = _id
        self.virtual_factory = virtual_factory
        if fetched_data is None:
            self.last_hist_seq = None
        else:
            self.last_hist_seq = fetched_data['last_hist_seq']

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'

    def __eq__(self, other):
        if not type(self) is type(other):
            return False
        else:
            return self.id == other.id and self.last_hist_seq == other.last_hist_seq


class SublotProduct(Product):
    def get_sts_data(self, column_name: str):
        if column_name in self.fetched_data:
            return self.fetched_data[column_name]
        else:
            # Assuming this method should fetch data if not found in fetched_data.
            fetched_data_dict = mes_db_query.get_sublot_sts_cross_factory(self.id)
            self.fetched_data = fetched_data_dict
            return self.fetched_data[column_name]

    @cached_property
    def lot(self) -> 'Lot':
        return Lot(self.get_sts_data('lot_id'), self.virtual_factory)

    @cached_property
    def wafering_segment(self) -> 'WaferingSegment':
        return WaferingSegment(self.get_sts_data('sublot_cmf_2'), common.ProductObjectType.WAFERING_SEGMENT,
                               self.virtual_factory)

    @cached_property
    def growing_segment(self) -> 'GrowingSegment':
        return self.wafering_segment.growing_segment

    @cached_property
    def ingot(self) -> 'Ingot':
        return Ingot(self.get_sts_data('sublot_cmf_1')[:-2], common.ProductObjectType.INGOT, self.virtual_factory)


class Sublot(SublotProduct):
    pass


class LotLikeProduct(Product):
    """
    Ingot -> GrowingSegment -> WaferingSegment -> Lot -> Sublot
    """

    # ingot lot segment
    @abstractmethod
    def sublot_list(self) -> List[Sublot]:
        ...


class Lot(LotLikeProduct):
    @functools.cached_property
    def sublot_list(self) -> List[Sublot]:
        sublot_sts = mes_db_query.get_sublot_sts_by_lot_id(self.id, self.virtual_factory)
        sublot_list = []
        for _index, data_row in sublot_sts.iterrows():
            sublot_list.append(Sublot(data_row['sublot_id'],
                                      self.virtual_factory, data_row.to_dict()))
        return sublot_list

    @functools.cached_property
    def growing_segment_list(self) -> List['GrowingSegment']:
        return_list = []
        for sublot in self.sublot_list:
            growing_segment = sublot.growing_segment
            if growing_segment not in return_list:
                return_list.append(growing_segment)
        return return_list

    @functools.cached_property
    def wafering_segment_list(self) -> List['GrowingSegment']:
        return_list = []
        for sublot in self.sublot_list:
            wafering_segment = sublot.wafering_segment
            if wafering_segment not in return_list:
                return_list.append(wafering_segment)
        return return_list

    @functools.cached_property
    def ingot_list(self) -> List['Ingot']:
        return_list = []
        for sublot in self.sublot_list:
            ingot = sublot.ingot
            if ingot not in return_list:
                return_list.append(ingot)
        return return_list


class WaferingSegment(LotLikeProduct):
    @cached_property
    def sublot_list(self) -> List[Sublot]:
        return_list = []
        sublot_df = mes_db_query.get_sublot_sts_by_wafering_segment_id_cross_factory(self.id)
        for _index, data_row in sublot_df.iterrows():
            return_list.append(Sublot(data_row['sublot_id'],
                                      self.virtual_factory, data_row.to_dict()))
        return return_list

    @cached_property
    def growing_segment(self) -> 'GrowingSegment':
        growing_segment_id = mes_db_query.get_growing_segment_id_cross_factory(self.id)
        return GrowingSegment(growing_segment_id, self.virtual_factory)

    @cached_property
    def ingot(self) -> 'Ingot':
        ingot_id = self.id[:-2]
        return Ingot(ingot_id, self.virtual_factory)


class GrowingSegment(LotLikeProduct):
    @cached_property
    def sublot_list(self) -> List[Sublot]:
        return_list = []
        for wafering_segment in self.wafering_segment_list:
            return_list.extend(wafering_segment.sublot_list)
        return return_list

    @cached_property
    def wafering_segment_list(self) -> List['WaferingSegment']:
        wafering_segment_id_list = mes_db_query.get_wafering_segment_id_list_cross_factory(self.id)
        return_list = []
        for wafering_segment_id in wafering_segment_id_list:
            return_list.append(WaferingSegment(wafering_segment_id,
                                               self.virtual_factory))
        return return_list

    def ingot(self) -> 'Ingot':
        return Ingot(self.id[:-2], self.virtual_factory)


class Ingot(LotLikeProduct):
    @cached_property
    def sublot_list(self) -> List[Sublot]:
        return_list = []
        for _index, data_row in mes_db_query.get_sublot_sts_by_ingot_id_cross_factory(self.id).iterrows():
            return_list.append(Sublot(data_row['sublot_id'],
                                      self.virtual_factory, data_row.to_dict()))
        return return_list

    @cached_property
    def growing_segment_list(self) -> List[GrowingSegment]:
        growing_segment_id_list = mes_db_query.get_growing_segment_id_list_by_ingot_id_cross_factory(self.id)
        return_list = []
        for growing_segment_id in growing_segment_id_list:
            return_list.append(GrowingSegment(growing_segment_id, self.virtual_factory))
        return return_list

    @cached_property
    def wafering_segment_list(self) -> List[WaferingSegment]:
        return_list = []
        for growing_segment in self.growing_segment_list:
            return_list.extend(growing_segment.wafering_segment_list)
        return return_list


class ContainmentBaseRule:
    def __init__(self, rule_orm: containment_model.ContainmentBaseRule):
        self.containment_base_rule_orm = rule_orm
        self.rule_name = rule_orm.rule_name
        self.rule_class = rule_orm.rule_class
        self.rule_data = rule_orm.rule_data
        self.rule_description = rule_orm.description
        self.virtual_factory = rule_orm.virtual_factory
        self.rule_sql = rule_orm.rule_sql

    def __repr__(self):
        return f'{self.__class__.__name__}({self.rule_name})'


class ContainmentRule:
    def __init__(self, rule_orm: containment_model.ContainmentRule):
        self.containment_rule_orm = rule_orm
        self.rule_name = rule_orm.rule_name
        self.rule_dict = rule_orm.rule_data
        self.rule_description = rule_orm.rule_description

    def __repr__(self):
        return f'{self.__class__.__name__}({self.rule_name})'

    @cached_property
    def all_base_classes(self):
        pass
