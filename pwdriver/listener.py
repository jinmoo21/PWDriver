from selenium.webdriver.support.abstract_event_listener import AbstractEventListener

from pwdriver.util import get_logger


logger = get_logger('listener')


class EventListener(AbstractEventListener):
    def before_navigate_to(self, url, driver) -> None:
        logger.info(f'{driver.current_url} -> {url}')

    def after_navigate_to(self, url, driver) -> None:
        logger.info(f'{driver.current_url}')

    def before_navigate_back(self, driver) -> None:
        logger.info(f'{driver.current_url} -> history.back')

    def after_navigate_back(self, driver) -> None:
        logger.info(f'{driver.current_url}')

    def before_navigate_forward(self, driver) -> None:
        logger.info(f'{driver.current_url} -> history.forward')

    def after_navigate_forward(self, driver) -> None:
        logger.info(f'{driver.current_url}')

    def before_find(self, by, value, driver) -> None:
        logger.info(f'{by}: {value}')

    def before_click(self, element, driver) -> None:
        logger.info(f'tag: {element.tag_name}({element.location})')

    def before_change_value_of(self, element, driver) -> None:
        logger.info(f'{element.text}')

    def after_change_value_of(self, element, driver) -> None:
        logger.info(f'{element.text}')

    def before_execute_script(self, script, driver) -> None:
        logger.info(f'{script}')
