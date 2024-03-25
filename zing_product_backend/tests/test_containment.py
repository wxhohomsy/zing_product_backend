import pandas as pd
from pytest import fixture
from zing_product_backend.core.product_containment.parser_core import containment_structure
from zing_product_backend.core.product_containment.parser_core.containment_structure import Sublot
from zing_product_backend.core import common
from zing_product_backend.app_db import mes_db_query


@fixture(scope='module')
def ingot_data():
    ingot_id = 'D03400'
    return containment_structure.Ingot(ingot_id, common.ProductObjectType.INGOT, common.VirtualFactory.L1W)


@fixture(scope='module')
def growing_segment_data():
    growing_segment_id = 'D2943005'
    growing_segment_data = containment_structure.GrowingSegment(growing_segment_id,
                                                                common.ProductObjectType.GROWING_SEGMENT,
                                                                common.VirtualFactory.L1W)
    return growing_segment_data


def mock_get_sublot_sts_by_lot_id(lot_id: str, virtual_factory: common.VirtualFactory):
    return pd.DataFrame(
        {
            'lot_id': [lot_id] * 6,
            'sublot_id': ['D10510720112', 'D10510720301', 'D10510720701', 'E32030J80109',
                          'E32030J81501', 'D40550150108'],
        }
    )


@fixture(scope='function')
def lot_data(monkeypatch):
    lot_id = 'S-IE2HC1312D'
    monkeypatch.setattr(mes_db_query, 'get_sublot_sts_by_lot_id', mock_get_sublot_sts_by_lot_id)
    return containment_structure.Lot(lot_id, common.VirtualFactory.L2W, {})


class TestIngots:
    def test_growing_segments(self, ingot_data):
        growing_segment_id_set = {'D0340001', 'D0340005', 'D0340030', 'D0340072', 'D03400B3', 'D03400F5', 'D03400K6'}
        assert growing_segment_id_set == {segment.id for segment in ingot_data.growing_segment_list}

    def test_wafering_segments(self, ingot_data):
        wafering_segment_id_set = {'D0340001', 'D0340005', 'D0340015',
                                   'D0340030', 'D0340072', 'D03400B3', 'D03400F5', 'D03400K6'}
        assert wafering_segment_id_set == {segment.id for segment in ingot_data.wafering_segment_list}

    def test_total_wafer_count(self, ingot_data):
        total_wafer_count = 0
        for segment in ingot_data.growing_segment_list:
            for wafering_segment in segment.wafering_segment_list:
                total_wafer_count += len(wafering_segment.sublot_list)
        assert total_wafer_count == 1971

        assert len(ingot_data.sublot_list) == 1972


class TestGrowingSegments:
    def test_wafering_segments(self, growing_segment_data):
        wafering_segment_id_set = {'D2943005', 'D2943015'}
        assert wafering_segment_id_set == {segment.id for segment in growing_segment_data.wafering_segment_list}


class TestLot:
    # 'lot_id': [lot_id] * 5,
    # 'sublot_id': ['D10510720112', 'D10510720301', 'D10510720701', 'E32030J80109', 'E32030J81501', 'D40550150108'],
    def test_wafer_count(self, lot_data):
        assert len(lot_data.sublot_list) == 6

    def test_wafering_segments(self, lot_data):
        wafering_segment_id_set = {'D1051072', 'E32030J8', 'D4055015'}
        for wafering_segment_id in wafering_segment_id_set:
            wafering_segment = containment_structure.WaferingSegment(wafering_segment_id,
                                                                     common.ProductObjectType.WAFERING_SEGMENT,
                                                                     common.VirtualFactory.L2W)
            assert wafering_segment in lot_data.wafering_segment_list

    def test_growing_segments(self, lot_data):
        growing_segment_id_set = {'D1051072', 'E32030J8', 'D4055005'}
        for growing_segment_id in growing_segment_id_set:
            growing_segment = containment_structure.GrowingSegment(growing_segment_id,
                                                                   common.ProductObjectType.GROWING_SEGMENT,
                                                                   common.VirtualFactory.L2W)
            assert growing_segment in lot_data.growing_segment_list

    def test_ingot_in_lot(self, lot_data):
        ingot_id_set = {'D10510', 'E32030', 'D40550'}
        for ingot_id in ingot_id_set:
            ingot = containment_structure.Ingot(ingot_id, common.ProductObjectType.INGOT, common.VirtualFactory.L2W)
            assert ingot in lot_data.ingot_list


if __name__ == "__main__":
    pass