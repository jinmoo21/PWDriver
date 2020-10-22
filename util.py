import logging
import os

import val


def parse_boolean(arg):
    return arg.lower() in ['true', 'y', 'yes']


def set_file_executable(path):
    if os.path.isfile(path) and not os.access(path, os.X_OK):
        import stat
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)


def get_logger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)-5s [%(name)s] '
                                  '%(funcName)s(%(pathname)s:%(lineno)d): %(message)s')
    console = logging.StreamHandler()
    if not os.path.exists(val.LOG_DIR):
        os.makedirs(val.LOG_DIR)
    file_handler = logging.FileHandler(filename=f'{val.LOG_DIR}{os.path.sep}{val.LOG_FILE}{val.LOG}')
    console.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger
