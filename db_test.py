from sqlalchemy import select
from zing_product_backend.app_db import connections
from zing_product_backend.models import material_setting


async def tool_func(id: int):
    stmt = select(material_setting.MatDef).filter(
        material_setting.MatDef.id == id
    )
    async for s in connections.get_async_session():
        data = await s.execute(stmt)
        yield data.scalars().first().mat_id


async def main():
    async for x in tool_func(3):
        print(x)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())