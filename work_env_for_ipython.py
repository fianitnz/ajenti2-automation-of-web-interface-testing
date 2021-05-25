from selenium import webdriver
from selenium.webdriver.common.by import By


from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.color import Color

from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from test_autotest import Locators, LocatorsHeader, LocatorsContentLogin

import time

WINDOW_SIZE = (1024, 786)
HOST_NAME = 'qwerty'
SCHEME = 'http://'
HOST_ADDRES = '192.168.122.181:8000'
LOGIN_ROOT = ('root', 'qwerty')
LOGIN_QWERTY = ('qwerty', 'qwerty')
# DRIVER = None
DEFAULT_TIME = 4

DRIVERF = webdriver.Firefox(executable_path='../selenium/geckodriver-v0.29.1')

DRIVERF.set_window_size(*WINDOW_SIZE)
DRIVERF.set_window_position(600-(WINDOW_SIZE[0]/2), 0)

DRIVERF.get(SCHEME + HOST_ADDRES)
#DRIVERF.get('file:///mnt/base/projekts/testing/ajenti/test.html')

C_OPT = webdriver.ChromeOptions()
C_OPT.add_experimental_option("excludeSwitches", ['enable-automation'])
# driver = webdriver.Chrome(options=C_OPT)
DRIVERC = webdriver.Chrome(
        executable_path='../selenium/chromedriver-v90.0.4430.24',
        options=C_OPT)

# fix_crutch resize bug
DRIVERC.maximize_window()

DRIVERC.set_window_size(*WINDOW_SIZE)
DRIVERC.set_window_position(600-(WINDOW_SIZE[0]/2), 0)

DRIVERC.get(SCHEME + HOST_ADDRES)
#DRIVERC.get('file:///mnt/base/projekts/testing/ajenti/test.html')


# def scr():
    #DRIVERF.refresh()
    #DRIVERC.refresh()

    #floc = DRIVERF.find_element(By.XPATH, '//div/input')
    #floc.click()
    #floc.screenshot('locF.png')

    #cloc = DRIVERC.find_element(By.XPATH, '//div/input')
    #cloc.click()
    #cloc.screenshot('locC.png')

floc = DRIVERF.find_element(By.XPATH, '//div/input')
cloc = DRIVERC.find_element(By.XPATH, '//div/input')

#floc.click()
#print('c')
#time.sleep(3)
#ActionChains(DRIVERF).send_keys(Keys.TAB).perform()
#print('c')
#time.sleep(3)
#ActionChains(DRIVERF).send_keys(Keys.TAB).perform()
#print('c')
#time.sleep(3)
#ActionChains(DRIVERF).send_keys(Keys.TAB).perform()
#print('c')
#time.sleep(3)
#ActionChains(DRIVERF).key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
#print('c')
#time.sleep(3)
#ActionChains(DRIVERF).key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
#print('c')
#time.sleep(3)
#ActionChains(DRIVERF).key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()

#cloc.click()
#print('c')
#time.sleep(3)
#ActionChains(DRIVERC).send_keys(Keys.TAB).perform()
#print('c')
#time.sleep(3)
#ActionChains(DRIVERC).send_keys(Keys.TAB).perform()
#print('c')
#time.sleep(3)
#ActionChains(DRIVERC).send_keys(Keys.TAB).perform()
#time.sleep(3)
#ActionChains(DRIVERC).key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
#print('c')
#time.sleep(3)
#ActionChains(DRIVERC).key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
#print('c')
#time.sleep(3)
#ActionChains(DRIVERC).key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
#print('c')
# class LocatorsHeader():
#    header = (By.XPATH, '//nav')
#    link_ajenti = (By.XPATH, '//nav//a[contains(., "Ajenti")]')
#    icon_host_name = (By.XPATH, '//nav//p[contains(., "qwerty")]')
#    menu_user_menu = None
#    button_resize =(By.XPATH, '//nav//a[@*="toggleWidescreen()"]')


# class Locators():
#    body = (By.TAG_NAME, 'BODY')






































#DRIVER.quit()
