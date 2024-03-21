from zing_product_backend.celery_app.test_update_lot import update_lot_main
import asyncio
from zing_product_backend.app_db import external_tables
from sqlalchemy import select, text
from zing_product_backend.app_db.mes_db_query import get_cdb_engine
from zing_product_backend.app_db.connections import l2w_db_engine


def test_sql():
    dd = "(mat_id like '%246%')"
    sql = text(rf"""
    SELECT 1 FROM MESMGR.mwipmatdef 
    WHERE 1 = 1 
    AND {dd}
    """)
    with l2w_db_engine.connect() as c:
        print(c.execute(sql).fetchall())


if __name__ == "__main__":
    test_sql()
