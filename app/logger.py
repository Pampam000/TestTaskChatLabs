import sys
from logging import getLogger, StreamHandler, Formatter, DEBUG

log_format = '%(asctime)s [%(levelname)s][%(pathname)s: %(funcName)s: ' \
             '%(lineno)d]: %(message)s'

stream_handler = StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(Formatter(fmt=log_format))

logger = getLogger(__name__)
logger.setLevel(DEBUG)

logger.addHandler(stream_handler)
