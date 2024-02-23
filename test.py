from zing_product_backend.celery_app.test_update_lot import update_lot_main
import asyncio

if __name__ == "__main__":
    asyncio.run(update_lot_main())
