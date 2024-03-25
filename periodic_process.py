from zing_product_backend.celery_app.test_update_lot import update_lot_main
import asyncio


async def main():
    await asyncio.gather(update_lot_main())

if __name__ == "__main__":
    import time
    asyncio.run(update_lot_main())
