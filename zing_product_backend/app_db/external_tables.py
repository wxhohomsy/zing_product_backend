from sqlalchemy import Table, MetaData
from zing_product_backend.app_db.connections import l1w_db_engine

mes_meta_data = MetaData()
mwipsltsts_l1w = Table("mwipsltsts", mes_meta_data, autoload_with=l1w_db_engine, schema='MESMGR')
mwiplotsts_l1w = Table("mwiplotsts", mes_meta_data, autoload_with=l1w_db_engine, schema='MESMGR')
mwipmatdef_l1w = Table("mwipmatdef", mes_meta_data, autoload_with=l1w_db_engine, schema='MESMGR')