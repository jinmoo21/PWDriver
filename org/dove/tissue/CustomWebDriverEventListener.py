from datetime import datetime
import logging
from logging import INFO


from selenium.webdriver.support.abstract_event_listener import AbstractEventListener


class CustomWebDriverEventListener(AbstractEventListener):
    logger = logging.getLogger("WebDriverEventListener")
    logger.setLevel(level=logging.DEBUG)

    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(process)d --- %(threadName)s %(pathname)s: %(message)s')

    stream_handler = logging.StreamHandler()
    # file_handler = logging.FileHandler(filename='./logs/' + datetime.now().strftime('%Y-%m-%d') + '.log')

    stream_handler.setFormatter(fmt=formatter)
    # file_handler.setFormatter(fmt=formatter)

    logger.addHandler(hdlr=stream_handler)

    # logger.addHandler(hdlr=file_handler)

    def before_navigate_to(self, url, driver):
        logging.info('hi')

    def before_navigate_back(self, driver):
        logging.info()

    def before_navigate_forward(self, driver):
        logging.info()

    def before_find(self, by, value, driver):
        logging.info(str(by))

    def before_click(self, element, driver):
        logging.info(str(element))

    def before_change_value_of(self, element, driver):
        logging.info(str(element))

    def before_execute_script(self, script, driver):
        logging.info(script)