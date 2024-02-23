from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import oracledb
from zing_product_backend import settings

oracledb.init_oracle_client()
load_dotenv()
l1w_db_engine = create_engine(os.environ.get('L1W_MESDB_URL'), pool_size=2, pool_pre_ping=True)
l2w_db_engine = create_engine(os.environ.get('L2W_MESDB_URL'), pool_size=2, pool_pre_ping=True)
app_db_engine = create_engine(os.environ.get('APP_DATABASE_URL'), pool_size=2)
app_async_engine = create_async_engine(os.environ.get('APP_ASYNC_DATABASE_URL'), pool_size=2, pool_pre_ping=True)
shaiapp02_client = MongoClient(os.environ.get('KLARF_DATABASE_URL'))
klarf_data_cache_collection = shaiapp02_client.measurement_equipment_db.klarf_data_cache_collection


AppSession = sessionmaker(app_db_engine, expire_on_commit=False)
AsyncAppSession = async_sessionmaker(app_async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncAppSession() as session:
        try:
            yield session
        finally:
            await session.commit()
            await session.close()


class Base(DeclarativeBase):
    __table_args__ = {"schema": "test"}
    pass


if __name__ == "__main__":
    import asyncio
    from sqlalchemy import text
    import pandas as pd

    sql = text(rf"""select * from prod.wafer_oper_history
        where sublot_id = 'D42210J50214'
    """)

    def select_data(session):
        with session.connection() as conn:
            df = pd.read_sql(sql, conn)
            print(df)

    async def main():
        async for s in get_async_session():
            # r = await s.execute(sql)
            # print(r.fetchall())
            await s.run_sync(select_data)
    asyncio.run(main())
