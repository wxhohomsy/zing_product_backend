from zing_product_backend.celery_app.test_update_lot import update_lot_main
import asyncio
from zing_product_backend.app_db import external_tables
from sqlalchemy import select, text
from zing_product_backend.app_db.mes_db_query import get_cdb_engine
from zing_product_backend.app_db.connections import l2w_db_engine
# from zing_product_backend.core.product_containment.containment_base_rules import mesdb_query, local_db_query
from zing_product_backend.app_db.mes_db_query import get_spec_by_material_and_operation
from zing_product_backend.core.common import VirtualFactory
import time
from zing_product_backend.core.product_containment.crud import get_ooc_spec_with_containment_id

if __name__ == "__main__":
    s = time.time()
    # virtual_factory = VirtualFactory.L2W
    # print(get_spec_by_material_and_operation('3PBCXPE188A', '2920', virtual_factory).columns)

    print(get_ooc_spec_with_containment_id())
    print(rf'Execution time: {time.time() - s} seconds')