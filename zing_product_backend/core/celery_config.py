import os
enable_utc = True
timezone = 'Asia/Shanghai'
broker_connection_retry_on_startup = True
broker_url = os.environ['DATA_VIEW_BROKER_URL']
result_backend = os.environ['DATA_VIEW_RESULT_BACKEND']
accept_content = ['json', 'pickle', 'msgpack']
result_accept_content = ['json', 'pickle', 'msgpack']
task_serializer = 'pickle'
result_serializer = 'pickle'
redis_max_connections = 400
redis_socket_connect_timeout = 100  # seconds
task_time_limit = 300  # seconds
result_expires = 60 * 60 * 4  # 4 hours
result_backend_max_retries = 100
default_task_priority = 5

beat_schedule = {

}