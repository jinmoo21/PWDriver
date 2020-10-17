from selenium.webdriver.support.abstract_event_listener import AbstractEventListener


class CustomWebDriverEventListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        print('hi')

    def before_navigate_back(self, driver):
        print('hi')

    def before_navigate_forward(self, driver):
        print('hi')

    def before_find(self, by, value, driver):
        print('hi')

    def before_click(self, element, driver):
        print('hi')

    def before_change_value_of(self, element, driver):
        print('hi')

    def before_execute_script(self, script, driver):
        print('hi')