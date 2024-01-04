from sqlalchemy import select
from zing_product_backend.app_db import connections
from zing_product_backend.models import material_setting


async def tool_func(input_id: int):
    stmt = select(material_setting.MatDef).filter(
        material_setting.MatDef.mat_id == input_id
    )
    async for s in connections.get_async_session():
        data = await s.execute(stmt)
        return data.scalars().first().mat_id


async def main():
    async for s in connections.get_async_session():
        stmt = select(material_setting.MatDef).filter()
        data = await s.execute(stmt)
        print(data.scalars().first().mat_id)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())