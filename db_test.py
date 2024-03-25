from sqlalchemy import select
from zing_product_backend.app_db import connections, mes_db_query
from zing_product_backend.models import general_settings, containment_model
from zing_product_backend.core.product_containment import crud
import db_init


async def main():
    async for s in connections.get_async_session():
        stmt = select(containment_model.ContainmentBaseRule).filter(
            containment_model.ContainmentBaseRule.rule_name.in_(('nast', ))

        )
        data_list = (await s.execute(stmt)).scalars().all()
        for data in data_list:
            print(data.rule_data)


if __name__ == "__main__":
    # import asyncio
    # asyncio.run(main())
    print(mes_db_query.get_sublot_sts_by_wafering_segment_id_cross_factory('E28030L5'))