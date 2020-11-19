import os
import logging

from logging.handlers import RotatingFileHandler
from logging import StreamHandler

from app.infrastructure.config import app_config


def create_logger():
    _logger = logging.getLogger(app_config.LOGGER_NAME)
    _logger.setLevel(logging.INFO)
    os.makedirs(app_config.LOG_FOLDER, exist_ok=True)
    fh = RotatingFileHandler(app_config.LOG_FILE_PATH, maxBytes=10240, backupCount=10)
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s : %(lineno)d ]'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    _logger.addHandler(fh)
    st = StreamHandler()
    st.setFormatter(formatter)
    _logger.addHandler(st)
    return _logger


logger = create_logger()
