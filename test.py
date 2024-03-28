import pandas as pd

from zing_product_backend.celery_app.test_update_lot import update_lot_main
import asyncio
from zing_product_backend.app_db import external_tables
from sqlalchemy import select, text
from zing_product_backend.app_db.mes_db_query import get_cdb_engine, get_csamspcdat_data, get_tqs_summary_data
from zing_product_backend.app_db.connections import l2w_db_engine
# from zing_product_backend.core.product_containment.containment_base_rules import mesdb_query, local_db_query
from zing_product_backend.app_db.mes_db_query import get_spec_by_material_and_operation
from zing_product_backend.core.common import VirtualFactory
from zing_product_backend.core.product_containment.containment_base_rules import containment_mesdb_query
from zing_product_backend.core.product_containment.parser_core.containment_structure import SublotProduct
import time
from zing_product_backend.core.product_containment.crud import get_ooc_spec_with_containment_id


def test_get_tqs_summary_data():
    pass


def test_csamspcdat_data():
    virtual_factory = VirtualFactory.L2W
    sublot_id = 'D31520G41008'
    oper_id = ('2920', '6700')
    print(get_csamspcdat_data('E03100J7', 'SEGMENT', spec_id=None,
                              virtual_factory=VirtualFactory.L2W,
                              oper_id='2900'
                              ))


def test_tqs_summary_data():
    virtual_factory = VirtualFactory.L2W
    sublot_id = 'D31520G41008'
    print(get_tqs_summary_data(sublot_id,spec_id='2920-A1', oper_id=None, virtual_factory=virtual_factory))


def test_get_spc_df():
    v_factory = VirtualFactory.L1W
    sublot = SublotProduct('D31520G41008', v_factory)

    spec_id_df = pd.DataFrame({
        'spec_id': ('6700-AreaCount', '6700-DCOAreaCountLLS1000', '2900-BULKFEMAXSE',
                    '2900-BULKFEMAXTE', '2900-CTRCARBTE', '2900-CTRRESSE', '2900-OISFSE')
    })
    print(containment_mesdb_query.get_spec_value_df(spec_id_df, sublot))


if __name__ == "__main__":
    s = time.time()
    # virtual_factory = VirtualFactory.L2W
    # print(get_spec_by_material_and_operation('3PBCXPE188A', '2920', virtual_factory).columns)

    # print(get_ooc_spec_with_containment_id())
    # test_csamspcdat_data()
    # test_csamspcdat_data_by_oper()
    # test_csamspcdat_data()
    # test_tqs_summary_data()
    test_get_spc_df()
    print(rf'Execution time: {time.time() - s} seconds')