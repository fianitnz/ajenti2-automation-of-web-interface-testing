from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.color import Color

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


WINDOW_SIZE = (1024, 786)
HOST_NAME = 'qwerty'
SCHEME = 'http://'
HOST_ADDRES = '192.168.122.181:8000'
LOGIN_ROOT = ('root', 'qwerty')
LOGIN_QWERTY = ('qwerty', 'qwerty')
#DRIVER = None
DEFAULT_TIME = 4

DRIVER = webdriver.Firefox(executable_path='../selenium/geckodriver')
DRIVER.set_window_size(*WINDOW_SIZE)
DRIVER.set_window_position(600-(WINDOW_SIZE[0]/2), 0)

DRIVER.get(SCHEME + HOST_ADDRES)


class LocatorsHeader():
        header = (By.XPATH, '//nav')
        link_ajenti = (By.XPATH, '//nav//a[contains(., "Ajenti")]')
        icon_host_name = (By.XPATH, '//nav//p[contains(., "qwerty")]')
        menu_user_menu = None
        button_resize =(By.XPATH, '//nav//a[@*="toggleWidescreen()"]')


class Locators():
    body = (By.TAG_NAME, 'BODY')






































#DRIVER.quit()
