import os
from logging import Logger


def parse_boolean(arg: str) -> bool:
    return arg.lower() in ['true', 'y', 'yes']


def get_pattern_matched_file(path, regex) -> list:
    import re
    file_list = []
    pattern = re.compile(regex)
    for file in os.listdir(path):
        if pattern.match(file):
            file_list.append(file)
    return file_list


def set_file_executable(path) -> None:
    if os.path.isfile(path) and not os.access(path, os.X_OK):
        import stat
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)


def get_logger(name=None) -> Logger:
    import logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)-5s [%(name)s] '
                                  '%(funcName)s(%(pathname)s:%(lineno)d): %(message)s')
    console = logging.StreamHandler()
    from pwdriver.val import LOG_DIR, LOG_NAME, ROOT_DIR
    os.makedirs(os.path.join(ROOT_DIR, LOG_DIR), mode=0o777, exist_ok=True)
    file_handler = logging.FileHandler(os.path.join(ROOT_DIR, LOG_DIR, LOG_NAME))
    console.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger
