import logging
from logging import Logger
import os
from datetime import datetime

date = datetime.date(datetime.now()).strftime("%d_%m_%Y")

def create_logger():
    logger = Logger('logger')
    logger.setLevel(logging.DEBUG)
    # create a file handler
    if not os.path.exists('logs'):
        os.mkdir('logs')
    log_file = os.path.join('logs', f'{date}.log')
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
