from celery import Celery

celery_app = Celery("zing_product_backend")
celery_app.config_from_object("core.celery_config")