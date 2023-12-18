import logging
import sys
from zing_product_backend.core import settings

stdout_handler = logging.StreamHandler(sys.stdout)
server_logger = logging.getLogger('debug_logger')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
server_logger.addHandler(stdout_handler)

if settings.DEBUG:
    server_logger.setLevel(logging.DEBUG)
else:
    server_logger.setLevel(logging.WARNING)

