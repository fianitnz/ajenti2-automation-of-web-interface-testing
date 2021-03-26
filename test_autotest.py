import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

WINDOW_SIZE = (1024, 786)
HOST_NAME = 'qwerty'
SCHEME = 'http://'
HOST_ADDRES = '192.168.122.181:8000'
LOGIN_ROOT = ('root', 'qwerty')
LOGIN_QWERTY = ('qwerty', 'qwerty')
DRIVER = None

# Что то тут не так или автоюз или скоп не нужен.
@pytest.fixture(scope="module", autouse=True)
def init_driver0():
    global DRIVER
    DRIVER = webdriver.Firefox(executable_path='../selenium/geckodriver')
    DRIVER.set_window_size(*WINDOW_SIZE)
    DRIVER.set_window_position(600-(WINDOW_SIZE[0]/2), 0)
    yield
    # Этой хрени тут не должно быть, но пока так.
    import time
    time.sleep(1)
    DRIVER.quit()


class LocatorsHeader():
    def __init__(self):
        #self.header = DRIVER.find_element_by_class_name('navbar')
        #print(DRIVER.find_element_by_xpath('//nav//a[contains(., "Ajenti")]').get_attribute('outerHTML'))
        self.link_ajenti = DRIVER.find_element_by_xpath(
                                              '//nav//a[contains(., "Ajenti")]')
        self.icon_host_name = DRIVER.find_element_by_xpath(
                                              '//nav//p[contains(., "qwerty")]')
        try:
            self.menu_user_menu = DRIVER.find_element_by_xpath('')
        except NoSuchElementException:
            self.menu_user_menu = None
        self.button_resize = DRIVER.find_element_by_xpath(
                                            '//nav//a[@*="toggleWidescreen()"]')
    #def link_ajenti(self):
        #print('\nэто оно')
        #print(dir(self.header.find_element_by_link_text('Ajenti').parent))
              ##.get_attribute('innerHTML'))
        #return self.header.find_element_by_link_text('Ajenti')
    #def icon_host_name(self):
        #pass
    #def menu_user_menu(self):
        #pass
    #def button_resize(self):
        #pass


class LocatorsMenu():
    pass


class LocatorsContentLogin():
    # сделать логин методом? или наследуемым элементом...
    pass


# Element
class Link():
    def __init__(self, locator):
        self.locator = locator
        self.text = ''
    def click(self):
        pass
    def screenshot_no_mouse(self):
        pass
    def screenshot_on_mouse(self):
        pass


# Section
class Header():
    def __init__(self):
        self.locators = LocatorsHeader()
        self.link_ajenti = Link(self.locators.link_ajenti)
        self.icon_host_name = None
        self.menu_user_menu = None
        self.button_resize = None




class Menu():
    pass


class ContentLogin():
    # сделать логин методом? или наследуемым элементом...
    pass


class TestCase1():
    #@pytest.mark.skip('skip test open panel')
    def test_open_panel_1(self):
        DRIVER.set_page_load_timeout(3)
        try:
            DRIVER.get(SCHEME + HOST_ADDRES)
        except TimeoutException:
            assert False, 'TestCase1: время загрузки превышено'

        #expected_conditions.url_matches
        assert DRIVER.current_url == \
               SCHEME + HOST_ADDRES + '/view/login/normal', \
               'TestCase1: not open login page'

        #WebDriverWait(DRIVER, 2).until(expected_conditions.title_is(HOST_NAME))
        assert expected_conditions.title_is(HOST_NAME)

    def test_header_2(self):
        self.header = Header()








        if self.header.link_ajenti.text == 'Ajenit':
            print('link contains Ajenit')
        self.header.link_ajenti.click()





# открытие панели

# возможно наблюдение за ним через browsermob-proxy
# произошло перенарпавление

# панель открылась
#print(dir(browser))
#test1(browser)
