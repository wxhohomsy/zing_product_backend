import os
enable_utc = True
timezone = 'Asia/Shanghai'
broker_connection_retry_on_startup = True
broker_url = os.environ['ZING_PRODUCT_BROKER_URL']
result_backend = os.environ['ZING_PRODUCT_RESULT_BACKEND']
accept_content = ['json', 'pickle', 'msgpack']
result_accept_content = ['json', 'pickle', 'msgpack']
task_serializer = 'pickle'
result_serializer = 'pickle'
redis_max_connections = 400
redis_socket_connect_timeout = 100  # seconds
task_time_limit = 2000  # seconds
result_expires = 60 * 60 * 4  # 4 hours
result_backend_max_retries = 10
default_task_priority = 5


beat_schedule = {
    'lot_stack_map_image_make': {
        'task': 'data_view.spx.lot_stack_imaging',
        'schedule': 5,
    },
    'lot_stack_map_data_batch_abstract': {
        'task': 'data_view.spx.spx_stack_map_batch_abstract',
        'schedule': 600,
    },
}
worker_concurrency = 12