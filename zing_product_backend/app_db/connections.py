import asyncio

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.ext.asyncio import AsyncAttrs
l1w_db_engine = create_engine(os.environ.get('L1W_MESDB_URL'), pool_size=2)
l2w_db_engine = create_engine(os.environ.get('L2W_MESDB_URL'), pool_size=2)
app_db_engine = create_engine(os.environ.get('APP_DATABASE_URL'), pool_size=2)
app_async_engine = create_async_engine(os.environ.get('APP_ASYNC_DATABASE_URL'), pool_size=2)
shaiapp02_client = MongoClient(os.environ.get('KLARF_DATABASE_URL'))
klarf_data_cache_collection = shaiapp02_client.measurement_equipment_db.klarf_data_cache_collection


AppSession = sessionmaker(app_db_engine, expire_on_commit=False)
AsyncAppSession = async_sessionmaker(app_async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    __table_args__ = {"schema": "test"}
    pass


from sqlalchemy import text
sql = text(rf"""
SELECT * FROM prod.wafer_oper_history
 where 1 = 1
 and sublot_id = 'D41470050210'
""")


async def f():
    async with AsyncAppSession() as s:
        a = await s.execute(sql)
        print(a.scalars().fetchall())
        print(123)

if __name__ == "__main__":
    import time
    from sqlalchemy import text

    start_time = time.time()

    with AppSession() as session:
        con = session.connection()
    #
        result = con.execute(sql)
        print(result.fetchall())
    #
    # asyncio.run(f())


    print(f"--- {time.time() - start_time} seconds ---")