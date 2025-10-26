import logging
import os
from logging.handlers import TimedRotatingFileHandler

def init_logger():
    os.makedirs('logs', exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler('logs/app.log', when='midnight', backupCount=7, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
