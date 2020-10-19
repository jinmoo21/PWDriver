import logging
import os

dir_name = 'logs'
file_name = f'{dir_name}{os.path.sep}output.log'


def get_logger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)-5s [%(name)s] '
                                  '%(funcName)s(%(pathname)s:%(lineno)d): %(message)s')
    console = logging.StreamHandler()
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    file_handler = logging.FileHandler(filename=file_name)
    console.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger
