import logging
import sys

logger = logging.getLogger()
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s "
)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
logger.handlers = [file_handler, stream_handler]
logger.setLevel(logging.INFO)
