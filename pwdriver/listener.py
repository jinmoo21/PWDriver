from selenium.webdriver.support.abstract_event_listener import AbstractEventListener

from pwdriver.util import get_logger


logger = get_logger('listener')


class EventListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        logger.info(f'{driver.current_url} -> {url}')

    def before_navigate_back(self, driver):
        logger.info(f'{driver.current_url} -> history.back')

    def before_navigate_forward(self, driver):
        logger.info(f'{driver.current_url} -> history.forward')

    def before_find(self, by, value, driver):
        logger.info(f'{by}: {value}')

    def before_click(self, element, driver):
        logger.info(f'tag: {element.tag_name}({element.location})')

    def before_change_value_of(self, element, driver):
        logger.info(element.text)

    def before_execute_script(self, script, driver):
        logger.info(script)
