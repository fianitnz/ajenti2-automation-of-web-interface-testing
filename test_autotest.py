# ALERT ATTENTION DANGER HACK SECURITY
# BUG FIXME DEPRECATED TASK TODO TBD WARNING CAUTION NOLINT
# NOTE NOTICE TEST TESTING

import time
import pytest


from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.color import Color

from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


from screenshots_diff import PM


import selenium
print('\n', '___Selenium version:', selenium.__version__)

DRIVER = None
WINDOW_SIZE = (1024, 786)

SCHEME = 'http://'
HOST_ADDRES = '192.168.122.181:8000'
HOST_NAME = 'qwerty'
LOGIN_QWERTY = ('qwerty', 'qwerty')
LOGIN_ROOT = ('root', 'qwerty')

# американский английский, британский английский, нужно разнести
LOCALE = 'en'

# WebDriverWait
DEFAULT_TIME = 4

STACK = None

# for pixelmatch: max percentage of differences
# если установить 0 можно реализовать создание глобального эталона
# нужен подбор значения и\или
# указание для каждого конкретного случая пороговог значения
PERCENT = 0.0

# Что то тут не так scope autouse
@pytest.fixture(scope="module", autouse=True)
def init_driver_0():
    global DRIVER, STACK

    DRIVER = webdriver.Firefox(
       executable_path='../selenium/geckodriver-v0.29.1')

    ## Disable information bar
    #chrome_opt = webdriver.ChromeOptions()
    #chrome_opt.add_experimental_option(
        #"excludeSwitches",
        #['enable-automation'])
    #DRIVER = webdriver.Chrome(
        #executable_path='../selenium/chromedriver-v90.0.4430.24',
        #options=chrome_opt)

    ## fix_crutch resize bug
    #DRIVER.maximize_window()

    DRIVER.set_window_size(*WINDOW_SIZE)
    DRIVER.set_window_position(600-(WINDOW_SIZE[0]/2), 0)

    # WINDOW_SIZE for directory name
    pm = PM('{}x{}'.format(*WINDOW_SIZE), LOCALE)

    STACK = pm.stack

    yield
    DRIVER.quit()

    pm.stack.put(['_exit', None, None])

    # использовалось для отладки
    te = time.time()
    while pm.p.is_alive():
        time.sleep(0.1)
        print(pm.p.is_alive(), round(time.time() - te, 1))
    # print(pm.p.is_alive())

    pm.p.join()
    # pm.p.terminate()
    pm.p.close()


# #############################################################################
#
# Expected conditions customs
#
# #############################################################################

'''
Есть большое подозрение на то, что фактический цвет элемента так не поймать.
А в свойствах прописан тот который должен быть, но в момент анимации перехода
не факт что он будет на скриншоте. И все эти проверки добавляют только задержку
благодаря которой на скриншотах цвета соответствуют но если увеличится время
анимации это ожидание цвета не будет рабоать.
Решение:
Проверять цвет на самом скриншоте делая его раз за разом, что накладно...
Делать тоже самое в самом браузере при момощи js, что не сильно лучше.

Отключить анимацию что, я не смог реализовать. Частично реализовано через JS

Добавить фиксированную задержку, что костыль и подвержено багам при плавающем
времени анимации.
'''


def wait_color_element(locat_or_elm, css, color):
    '''
    locat_or_elm локатор элемента, элемент или tuple для поиска через js
    css имя свойства стиля в котором хранится цвет
    color цвет в формате rgba
    '''
    def _predicat_js_prop(driver):
        ret = driver.execute_script('''
            return window.getComputedStyle(document.querySelector('{}'), '{}')
            .getPropertyValue('{}');
            '''.format(element, pseudo_elem, prop))
        ret = Color.from_string(ret).rgba
        # print('факт', ret, 'долж', color, css)
        return ret == color

    def _predicat_tup(driver):
        item_color = Color.from_string(
            driver.find_element(*locat_or_elm)
            .value_of_css_property(css)).rgba
        # print('факт', item_color, 'долж', color, css)
        return item_color == color

    def _predicat(driver):
        item_color = Color.from_string(
            locat_or_elm
            .value_of_css_property(css)).rgba
        # print('факт', item_color, 'долж', color, css)
        return item_color == color
    # if type(css) == tuple:
    if isinstance(css, tuple):
        element, pseudo_elem, prop = css
        return _predicat_js_prop
    else:
        return _predicat_tup if type(locat_or_elm) == tuple else _predicat


# EC as https://github.com/SeleniumHQ/selenium/blob/trunk/py/selenium/
# webdriver/support/expected_conditions.py
def wait_color_locator(locator, css, color):
    def _predicat(driver):
        item_color = Color.from_string(driver.find_element(*locator)
                                       .value_of_css_property(css)).rgba
        return item_color == color
    return _predicat


# EC as https://stackoverflow.com/questions/19377437/
class WaitColor():
    def __init__(self, locator, css, color):
        self.locator = locator
        self.css = css
        self.color = color

    def __call__(self, driver):
        try:
            item_color = Color \
                .from_string(EC
                             ._find_element(driver, self.locator)
                             .value_of_css_property(self.css)).rgba
            return item_color == self.color
        except StaleElementReferenceException:
            return False


ecc_wait_color = wait_color_element


# для jquery есть .is(':animated') но что то не работает даже на демо
def ecc_wait_transform(element):
    def _predicat(driver):
        x, y = round(element.location['x']), round(element.location['y'])
        h, w = round(element.size['height']), round(element.size['width'])
        time.sleep(0.1)
        return x, y == round(element.location['x']), \
            round(element.location['y']) \
            and h, w == round(element.size['height']), \
            round(element.size['width'])
    return _predicat


def ecc_wait_css_js(selector, pseudo_elem, prop, equal):
    def _predicat(driver):
        ret = driver.execute_script('''
            return window.getComputedStyle(document.querySelector('{}'), '{}')
            .getPropertyValue('{}');
            '''.format(selector, pseudo_elem, prop))

        if ret.startswith('"') and ret.endswith('"'):
            ret = ret.strip('"')

        return ret == equal
    return _predicat


# #############################################################################
#
# Locators
#
# #############################################################################
class LocatorsHeader():
    header = (By.XPATH, '//nav')
    link_ajenti = (By.XPATH, '//nav//a[contains(., "Ajenti")]')
    icon_host_name = (By.XPATH, '//nav//p[contains(., "qwerty")]')
    menu_user_menu = None

    button_resize = (By.XPATH, '//nav//a[@*="toggleWidescreen()"]')
    button_resize_css = {
        'background': 'border-left-color',
        'icon': 'color'}
    button_resize_color = {
        'background': 'rgba(33, 150, 243, 1)',
        'background_mouse_on': 'rgba(207, 207, 207, 1)',  # over
        'background_mouse_hold': 'rgba(174, 174, 174, 1)',  # press
        'icon_mouse_on': 'rgba(33, 150, 243, 1)',  # over
        'icon_mouse_hold': 'rgba(51, 51, 51, 1)'}  # press


class LocatorsContentLogin():
    content_login = (By.XPATH, '//div[@id="login-form"]')

    icon_padlock = (By.XPATH, '//i[@class="fa fa-lock"]')
    icon_padlock_js = ('i.fa.fa-lock')
    icon_padlock_flip = (By.XPATH, '//i[@class="fa flip-cycle fa-lock"]')
    icon_padlock_flip_js = {'i.fa.flip-cycle.fa-lock'}
    icon_padlock_unlock = (
        By.XPATH, '//i[@class="fa flip-cycle fa-unlock-alt"]')
    icon_padlock_unlock_js = {'i.fa.flip-cycle.fa-unlock-alt'}
    icon_padlock_css = {'color': 'color'}
    icon_padlock_color = {'color': 'rgba(136, 136, 136, 1)'}

    # //input[contains(@*, "username")]
    # //input[@*[name()='ng:model']]
    # //input[@*[name()='ng:model'] and @*[contains(., 'username')]]
    field_usr = (By.XPATH, '//input[@placeholder="Username"]')
    field_usr_scr = (By.XPATH, '//input[@placeholder="Username"]/..')
    field_usr_css = {
        'background': 'background-color',
        'border_bottom': 'border-bottom-color',
        # костыль для получения значения псевдоэлемента через js
        'text_placeholder': ('input', '::placeholder', 'color'),
        'text': 'color'}
    field_usr_color = {
        'background': 'rgba(248, 248, 248, 1)',
        'background_click': 'rgba(255, 255, 255, 1)',
        'border_bottom': 'rgba(221, 221, 221, 1)',
        'border_bottom_click': 'rgba(33, 150, 243, 1)',
        'text_placeholder': 'rgba(153, 153, 153, 1)',
        'text': 'rgba(85, 85, 85, 1)'}

    # //input[contains(@*, "password")]
    field_pswd = (By.XPATH, '//input[@placeholder="Password"]')
    field_pswd_css = field_usr_css
    field_pswd_color = field_usr_color

    button_login = (By.XPATH, '//a[contains(., "Log in")]')
    button_login_css = {
        'background': 'background-color',
        'background_activ': 'border-top-color',
        'text': 'color'}
    button_login_color = {
        'background': 'rgba(33, 150, 243, 1)',
        'background_activ': 'rgba(10, 104, 180, 1)',
        'text': 'rgba(255, 255, 255, 1)'}

    # Лишняя обвязка к удалению
    #@classmethod
    #def field(self, typ):
        #if typ == 'usr':
            #return self.field_usr_css, self.field_usr_color
        #if typ == 'pswd':
            #return self.field_usr_css, self.field_usr_color
        #pass


class LocatorsMenu():
    pass


class Locators():
    body = (By.TAG_NAME, 'body')


# #############################################################################
#
# Modules
#
# #############################################################################
class Screenshot():
    def screenshot(self, id, note, src=True, locator=None, percent=PERCENT):
        ''' Порядок проверки локатора:
            1 локатор переданный
            2 локатор элемента
            3 локатор скриншота'''

        # Двойная проверка locator и locator_scr но частая
        # if locator is None and self.locator_scr is None:
        #    locator = self.locator
        # elif locator is None and self.locator_scr is not None:
        #    locator = self.locator_scr

        # Двойная перезапись locator но редкая
        if locator is None:
            locator = self.locator
            if self.locator_scr is not None:
                locator = self.locator_scr

        if src:
            img = WebDriverWait(DRIVER, DEFAULT_TIME) \
                .until(EC.visibility_of_element_located(locator)) \
                .screenshot_as_png
            STACK.put([img,
                      '{}_{}___{}___{}'.format(id,
                                               self.prefix,
                                               self.suffix,
                                               note),
                      percent])
        else:
            WebDriverWait(DRIVER, DEFAULT_TIME) \
                .until(EC.visibility_of_element_located(locator)) \
                .screenshot('{}_{}x{}_{}_{}.png'
                            .format(self.prefix,
                                    *WINDOW_SIZE,
                                    self.suffix,
                                    note)
                            )

    def screenshot_parent(self, id, note, src=True):
        self.screenshot(id, note, src, self.locator_parent)

    def screenshot_body(self, id, note, src=True):
        self.screenshot(id, note, src, Locators.body)


def get(url, anim=False):
    DRIVER.get(url)
    if not anim:
        DRIVER.execute_script('''
        let style = document.createElement('style');
        style.innerHTML = `
            body *,
            body * :after,
            body * :before {
            animation: none !important;
            transition: none !important;
            }
        `;
        document.head.appendChild(style);
        ''')


# #############################################################################
#
# Elements
#
# #############################################################################
class Link(Screenshot):
    def __init__(self, prefix, suffix, locator, locator_parent,
                 locator_scr=None):
        self.prefix = prefix
        self.suffix = suffix
        self.locator = locator
        self.locator_parent = locator_parent
        self.locator_scr = locator_scr

    def text_get(self):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .text

    def link_adders(self):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .get_attribute('href')

    def click(self):
        WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .click()

    def mouse_on(self):
        # Возможно нужно visibility_of_element_located
        element = WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator))
        ActionChains(DRIVER) \
            .move_to_element(element) \
            .perform()


class Icon(Screenshot):
    def __init__(self, prefix, suffix, locator, locator_js, locator_parent,
                 locator_scr=None):
        self.prefix = prefix
        self.suffix = suffix
        self.locator = locator
        self.locator_js = locator_js
        self.locator_parent = locator_parent
        self.locator_scr = locator_scr

    def color(self, css, color):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(ecc_wait_color(self.locator, css, color))

    def css(self, name):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .value_of_css_property(name)

    def css_js(self, pseudo_elem, prop, equal):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(ecc_wait_css_js(
                self.locator_js,
                pseudo_elem,
                prop,
                equal))

    def is_visible(self):
        ret = WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(EC.visibility_of_element_located(self.locator))
        return True if ret is not None else False


class IconWithName(Screenshot):
    def __init__(self, prefix, suffix, locator, locator_parent,
                 locator_scr=None):
        self.prefix = prefix
        self.suffix = suffix
        self.locator = locator
        self.locator_parent = locator_parent
        self.locator_scr = locator_scr

    def text_get(self):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .text


class Button(Screenshot):
    def __init__(self, prefix, suffix, locator, locator_parent,
                 locator_scr=None):
        self.prefix = prefix
        self.suffix = suffix
        self.locator = locator
        self.locator_parent = locator_parent
        self.locator_scr = locator_scr

    def css(self, name):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .value_of_css_property(name)

    def attribute(self, name):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .get_attribute(name)

    def color(self, css, color):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(ecc_wait_color(self.locator, css, color))

    def text_get(self):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .text

    def mouse_on(self):
        # Возможно нужно visibility_of_element_located
        element = WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator))
        ActionChains(DRIVER) \
            .move_to_element(element) \
            .perform()

    def mouse_on_wait_color(self, css, color):
        element = WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator))
        ActionChains(DRIVER) \
            .move_to_element(element) \
            .perform()
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(ecc_wait_color(element, css, color))

    def click_hold_wait_transform(self):
        element = WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator))
        ActionChains(DRIVER) \
            .click_and_hold(element) \
            .perform()
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(ecc_wait_transform(element))

    def click_hold_wait_color(self, css, color):
        element = WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator))
        ActionChains(DRIVER) \
            .click_and_hold(element) \
            .perform()
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(ecc_wait_color(element, css, color))

    def click_hold(self):
        element = WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator))
        ActionChains(DRIVER) \
            .click_and_hold(element) \
            .perform()

    def click(self):
        WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .click()

    def key_comb(self, mod, key):
        ActionChains(DRIVER) \
            .key_down(mod) \
            .send_keys(key) \
            .key_up(mod) \
            .perform()

    def reset_wait_color(self, css, color):
        ActionChains(DRIVER).reset_actions()
        ActionChains(DRIVER) \
            .move_to_element_with_offset(DRIVER.find_element(*Locators.body),
                                         0, 0) \
            .click() \
            .perform()
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(ecc_wait_color(self.locator, css, color))

    def element_on_focus(self):
        # js documet.activeElement
        # проверить скорость выполнения с промежуточным присвоением и
        # вычислением на месте
        element = DRIVER.find_element(*self.locator).id
        active = DRIVER.switch_to.active_element.id
        return True if element == active else False


class Field(Screenshot):
    def __init__(self, prefix, suffix, locator, locator_parent,
                 locator_scr=None):
        self.prefix = prefix
        self.suffix = suffix
        self.locator = locator
        self.locator_parent = locator_parent
        self.locator_scr = locator_scr

    def attribute(self, name):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .get_attribute(name)

    def color(self, css, color):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(ecc_wait_color(self.locator, css, color))

    def click(self):
        WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .click()

    def click_wait_color(self, css, color):
        WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .click()
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(ecc_wait_color(self.locator, css, color))

    def text(self, text):
        WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .send_keys(text)

    def text_get(self):
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .get_attribute('value')

    def key(self, key):
        WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .send_keys(key)

    def key_wait_color(self, key, css, color):
        WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(lambda d: d.find_element(*self.locator)) \
            .send_keys(key)
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(ecc_wait_color(self.locator, css, color))

    def key_comb(self, mod, key):
        ActionChains(DRIVER) \
            .key_down(mod) \
            .send_keys(key) \
            .key_up(mod) \
            .perform()

    def element_on_focus(self):
        # js documet.activeElement
        # проверить скорость выполнения с промежуточным присвоением и
        # вычислением на месте
        element = DRIVER.find_element(*self.locator).id
        active = DRIVER.switch_to.active_element.id
        return True if element == active else False

    # def in_put(self, text, key):
        # element = WebDriverWait(DRIVER, DEFAULT_TIME) \
            # .until(lambda d: d.find_element(*self.locator))
        # ActionChains(DRIVER) \
            # .click(element) \
            # .send_keys(text) \
            # .send_keys(key) \
            # .perform()

    def reset_wait_color(self, css, color):
        ActionChains(DRIVER).reset_actions()
        ActionChains(DRIVER) \
            .move_to_element_with_offset(DRIVER.find_element(*Locators.body),
                                         0, 0) \
            .click() \
            .perform()
        return WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(ecc_wait_color(self.locator, css, color))


# #############################################################################
#
# Section
#
# #############################################################################
class Body(Screenshot):
    prefix = 'body'
    suffix = '0_body'
    locator = Locators.body
    locator_parent = locator
    locator_scr = locator


class Header(Screenshot):
    prefix = 'header'
    suffix = '0_header'
    locator = LocatorsHeader.header
    locator_parent = Locators.body
    locator_scr = locator

    link_ajenti = Link(prefix,
                       '1_link_ajenti',
                       LocatorsHeader.link_ajenti,
                       locator)
    icon_host_name = IconWithName(prefix,
                                  '2_icon_host_name',
                                  LocatorsHeader.icon_host_name,
                                  locator)
    button_resize = Button(prefix,
                           '3_button_resize',
                           LocatorsHeader.button_resize,
                           locator)


class ContentLogin(Screenshot):
    prefix = 'content_login'
    suffix = '0_content_login'
    locator = LocatorsContentLogin.content_login
    locator_parent = Locators.body
    locator_scr = locator

    icon_padlock = Icon(prefix,
                        '1_icon_padlock',
                        LocatorsContentLogin.icon_padlock,
                        LocatorsContentLogin.icon_padlock_js,
                        locator)
    icon_padlock_flip = Icon(
        prefix,
        '1_icon_padlock',
        LocatorsContentLogin.icon_padlock_flip,
        LocatorsContentLogin.icon_padlock_flip_js,
        locator)
    icon_padlock_unlock = Icon(
        prefix,
        '1_icon_padlock',
        LocatorsContentLogin.icon_padlock_unlock,
        LocatorsContentLogin.icon_padlock_unlock_js,
        locator)
    field_usr = Field(prefix,
                      '2_field_usr',
                      LocatorsContentLogin.field_usr,
                      locator,
                      LocatorsContentLogin.field_usr_scr)
    field_pswd = Field(prefix,
                       '3_field_pswd',
                       LocatorsContentLogin.field_pswd,
                       locator)

    # Лишняя обвязка к удалению
    #def field(self, typ):
        #if typ == 'usr':
            #return self.field_usr
        #if typ == 'pswd':
            #return self.field_pswd

    button_login = Button(prefix,
                          '4_button_login',
                          LocatorsContentLogin.button_login,
                          locator)


class Menu():
    pass


# #############################################################################
#
# Tests
#
# #############################################################################
class TestCase1():
    def test_open_panel_1_0(self):
        id = '1.0'
        body = Body()
        DRIVER.set_page_load_timeout(4)

        try:
            get(SCHEME + HOST_ADDRES)
        except TimeoutException:
            assert False, '1.0 Время загрузки страницы'

        # longfixme наблюдение за перенаправлением не реализовано
        # Проверка только по факту конечнго url
        # Возможна реализация с помощью browsermob-proxy

        # EC.url_matches
        # Нет ожидания появления, фз нужно ли оно тут.
        assert DRIVER.current_url == \
            SCHEME + HOST_ADDRES + '/view/login/normal', '1.0 Перенаправение'

        assert WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(EC.title_is(HOST_NAME)), '1.0 Имя хоста в заголовке'
        body.screenshot(id, '1_overview')

    def test_header_1_1(self):
        id = '1.1'
        header = Header()
        button_resize_css = LocatorsHeader.button_resize_css
        button_resize_color = LocatorsHeader.button_resize_color

        header.screenshot(id, '1_overview')

    # Link Ajenti
        # fixme двойная проверка на название, первая в локаторе
        assert header.link_ajenti.text_get() == \
            'Ajenti', '1.1 Текст ссылки "Ajenti"'
        assert header.link_ajenti.link_adders() == \
            SCHEME + HOST_ADDRES + '/view/', '1.1 Адрес ссылки "Ajenti"'

        header.link_ajenti.click()

        # longfixme перенаправление не реализовано
        # Нет ожидания появления, фз нужно ли оно тут.
        assert DRIVER.current_url == \
            SCHEME + HOST_ADDRES + '/view/login/normal', '1.1 Перенаправление'

        header.link_ajenti.screenshot_parent(id, '1_mouse_no')
        header.link_ajenti.mouse_on()
        header.link_ajenti.screenshot_parent(id, '2_mouse_on')

    # Icon host name
    # при меленьком разрешении иконка отсутствует, придумать обработчик.
        assert header.icon_host_name.text_get() == \
            HOST_NAME, '1.1 Иконка с именем хоста "{}"'.format(HOST_NAME)

        header.icon_host_name.screenshot_parent(id, '1_nothing')

    # Button resize
    # при меленьком разрешении кнопка отсутствует, придумать обработчик.
        header.button_resize.screenshot_parent(id, '1_mouse_no')
        assert header.button_resize.mouse_on_wait_color(
            button_resize_css['background'],
            button_resize_color['background_mouse_on'])
        header.button_resize.screenshot_parent(id, '2_mouse_on')
        header.button_resize.reset_wait_color(
            button_resize_css['background'],
            button_resize_color['background'])

        header.button_resize.screenshot_parent(id, '3_click_hold_no')
        assert header.button_resize.click_hold_wait_color(
            button_resize_css['background'],
            button_resize_color['background_mouse_hold'])
        header.button_resize.screenshot_parent(id, '4_click_hold_on')
        header.button_resize.reset_wait_color(
            button_resize_css['background'],
            button_resize_color['background'])

        header.button_resize.screenshot_body(id, '5_click_no')
        header.button_resize.click()
        header.button_resize.screenshot_body(id, '6_click_on')

    # Restore
        header.button_resize.click()

    def test_content_login_1_2(self):
        id = '1.2'
        content_login = ContentLogin()
        icon_padlock_css = LocatorsContentLogin.icon_padlock_css
        icon_padlock_color = LocatorsContentLogin.icon_padlock_color
        field_usr_css = LocatorsContentLogin.field_usr_css
        field_usr_color = LocatorsContentLogin.field_usr_color
        field_pswd_css = LocatorsContentLogin.field_pswd_css
        field_pswd_color = LocatorsContentLogin.field_pswd_color
        button_login_css = LocatorsContentLogin.button_login_css
        button_login_color = LocatorsContentLogin.button_login_color
        # к удалению
        #field_usr_css, field_usr_color = LocatorsContentLogin.field('usr')
        #field_pswd_css, field_pswd_color = LocatorsContentLogin.field('pswd')

        content_login.screenshot(id, '1_overview')

    # Icon padlock
        content_login.icon_padlock.screenshot_parent(id, '1_icon_padlock')
        assert content_login.icon_padlock.color(
            icon_padlock_css['color'],
            icon_padlock_color['color'])
        assert content_login.icon_padlock.css('font-size') == '48px'
        # смысла особого нет так как значок  не меняется в элементе, \
        # а проверять надо видимость но для разминки пойдет
        # utf= py='\uf023' py_js_return='"\f023"' js_console="\"\uf023\""
        assert content_login.icon_padlock.css_js(
            '::before', 'content', '\uf023')

##
##
##
    # Field user
        content_login.field_usr.screenshot(id, '1_mouse_no')
        # цвет светло серый
        assert content_login.field_usr.color(
            field_usr_css['background'],
            field_usr_color['background'])
        # надпись заполнитель Username
        assert content_login.field_usr.attribute('placeholder') == 'Username'
        # цвет надписи заполнителя серый
        # BUG в браузере Chrome, не реализовано
        # assert content_login.field_usr.color(
        #    field_usr_css['text_placeholder'],
        #    field_usr_color['text_placeholder'])
        # нижний бордер серый
        assert content_login.field_usr.color(
            field_usr_css['border_bottom'],
            field_usr_color['border_bottom'])
        # при наведении:
        # курсор текст
        assert content_login.field_usr.attribute('type') == 'text'

        # при клике:
        # цвет меняется на фоновый
        assert content_login.field_usr.click_wait_color(
            field_usr_css['background'],
            field_usr_color['background_click'])
        content_login.field_usr.screenshot(id, '2_click')
        # фокус на элементе
        assert content_login.field_usr.element_on_focus()
        # нижний бордер синий
        assert content_login.field_usr.color(
            field_usr_css['border_bottom'],
            field_usr_color['border_bottom_click'])

        # при вводе:
        content_login.field_usr.text(LOGIN_QWERTY[0])
        # исчезает надпись Username
        # выводятся набираемые символы
        # поле содержит набранные символы
        assert content_login.field_usr.text_get() == LOGIN_QWERTY[0]
        content_login.field_usr.screenshot(id, '3_input')
        # цвет символов черный
        assert content_login.field_usr.color(
            field_usr_css['text'],
            field_usr_color['text'])
        # клавиша Backspase удаляет введенные символы
        content_login.field_usr.key(Keys.BACKSPACE)
        # поле содержит набранные символы минус количество нажатий Backspase
        assert content_login.field_usr.text_get() == LOGIN_QWERTY[0][0:-1]
        content_login.field_usr.screenshot(id, '4_backspace')
        # при удалении всех сиволов появляется надпись Username
        content_login.field_usr.key(Keys.BACKSPACE*len(LOGIN_QWERTY[0][0:-1]))
        content_login.field_usr.screenshot(id, '5_clear')
        # клавиша Tab переводит фокус к следующему элементу
        content_login.field_usr.key(Keys.TAB)
        assert not content_login.field_usr.element_on_focus()
        # скриншот смены фокуса в следующем блоке
        # что бы не дублировать проверку цвета

        # при потере фокуса:
        # исходное состояние
        assert content_login.field_usr.color(
            field_usr_css['background'],
            field_usr_color['background'])
        assert content_login.field_usr.color(
            field_usr_css['border_bottom'],
            field_usr_color['border_bottom'])
        content_login.field_usr.screenshot_parent(id, '6_next_focus')
        content_login.field_usr.screenshot(id, '7_no_write')
        # набранные символы если введены
        content_login.field_usr.text(LOGIN_QWERTY[0])
        assert content_login.field_usr.text_get() == LOGIN_QWERTY[0]
        content_login.field_usr.screenshot(id, '8_write')

        # Restore
        content_login.field_usr.key(Keys.CONTROL+Keys.BACKSPACE)

        # Вариант признан накладным, вводящим лишние проверки и обвязку для
        # работы, втч передачу параметров.
        # Проще и надежнее обойтись дублированием кода, простое лучше сложного.
        # Хотя возможно такая реализация подойдет для более простых
        # и однородных повторяющихся более часто элементов.
        #a = (('usr', 'Username', 'text', LOGIN_QWERTY[0],
              #*LocatorsContentLogin.field('usr')),
             #('pswd', 'Password', 'password', LOGIN_QWERTY[1],
              #*LocatorsContentLogin.field('pswd')))
        #for i in a:
            #typ, placeholder, attribute, inp, css, color = i
    # Field user and password
            #content_login.field(typ).screenshot(id, '1_mouse_no')
            ## цвет светло серый
            #assert content_login.field(typ).color(
                #css['background'],
                #color['background'])
            ## надпись заполнитель Username
            #assert content_login.field(typ).attribute('placeholder') \
                #== placeholder
            ## цвет надписи заполнителя серый
            #assert content_login.field(typ).color(
                #css['text_placeholder'],
                #color['text_placeholder'])
            ## нижний бордер серый
            #assert content_login.field(typ).color(
                #css['border_bottom'],
                #color['border_bottom'])
            ## при наведении:
            ## курсор текст
            #assert content_login.field(typ).attribute('type') == attribute

            ## при клике:
            ## цвет меняется на фоновый
            #assert content_login.field(typ).click_wait_color(
                #css['background'],
                #color['background_click'])
            #content_login.field(typ).screenshot(id, '2_click')
            ## фокус на элементе
            #assert content_login.field(typ).element_on_focus()
            ## нижний бордер синий
            #assert content_login.field(typ).color(
                #css['border_bottom'],
                #color['border_bottom_click'])

            ## при вводе:
            #content_login.field(typ).text(inp)
            ## исчезает надпись Username
            ## выводятся набираемые символы
            #content_login.field(typ).screenshot(id, '3_input')
            ## клавиша Backspase удаляет введенные символы
            #content_login.field(typ).key(Keys.BACKSPACE)
            #content_login.field(typ).screenshot(id, '4_backspace')
            ## при удалении всех сиволов появляется надпись Username
            #content_login.field(typ).key(
                #Keys.BACKSPACE*len(inp[0:-1]))
            #content_login.field(typ).screenshot(id, '5_clear')
            ## клавиша Tab переводит фокус к следующему элементу
            #content_login.field(typ).key(Keys.TAB)
            #assert not content_login.field(typ).element_on_focus()
            ## скриншот смены фокуса в следующем блоке
            ## что бы не дублировать проверку цвета

            ## при потере фокуса:
            ## исходное состояние
            #assert content_login.field(typ).color(
                #css['background'],
                #color['background'])
            #assert content_login.field(typ).color(
                #css['border_bottom'],
                #color['border_bottom'])
            #content_login.field(typ).screenshot_parent(id, '6_next_focus')
            #content_login.field(typ).screenshot(id, '7_no_write')
            ## черные символы если введены
            #content_login.field(typ).text(inp)
            #content_login.field(typ).screenshot(id, '8_write')

            ## Restore
            #content_login.field(typ).key(Keys.CONTROL+Keys.BACKSPACE)

    # Field password
        content_login.field_pswd.screenshot(id, '1_mouse_no')
        # цвет светло серый
        assert content_login.field_pswd.color(
            field_pswd_css['background'],
            field_pswd_color['background'])
        # надпись заполнитель Password
        assert content_login.field_pswd.attribute('placeholder') == 'Password'
        # цвет надписи заполнителя серый
        # BUG в браузере Chrome, не реализовано
        # assert content_login.field_pswd.color(
        #    field_pswd_css['text_placeholder'],
        #    field_pswd_color['text_placeholder'])
        # нижний бордер серый
        assert content_login.field_pswd.color(
            field_pswd_css['border_bottom'],
            field_pswd_color['border_bottom'])
        # при наведении:
        # курсор текст
        assert content_login.field_pswd.attribute('type') == 'password'

        # при клике:
        # цвет меняется на фоновый
        assert content_login.field_pswd.click_wait_color(
            field_pswd_css['background'],
            field_pswd_color['background_click'])
        content_login.field_pswd.screenshot(id, '2_click')
        # фокус на элементе
        assert content_login.field_pswd.element_on_focus()
        # нижний бордер синий
        assert content_login.field_pswd.color(
            field_pswd_css['border_bottom'],
            field_pswd_color['border_bottom_click'])

        # при вводе:
        content_login.field_pswd.text(LOGIN_QWERTY[1])
        # исчезает надпись Password
        # выводятся набираемые символы замененные на •
        # поле содержит набранные символы замененные на •
        assert content_login.field_pswd.text_get() == LOGIN_QWERTY[1]
        content_login.field_pswd.screenshot(id, '3_input')
        # цвет символов черный
        assert content_login.field_pswd.color(
            field_pswd_css['text'],
            field_pswd_color['text'])
        # клавиша Backspase удаляет введенные символы
        content_login.field_pswd.key(Keys.BACKSPACE)
        # поле содержит набранные символы минус количество нажатий Backspase
        assert content_login.field_pswd.text_get() == LOGIN_QWERTY[1][0:-1]
        content_login.field_pswd.screenshot(id, '4_backspace')
        # при удалении всех сиволов появляется надпись Password
        content_login.field_pswd.key(Keys.BACKSPACE*len(LOGIN_QWERTY[1][0:-1]))
        content_login.field_pswd.screenshot(id, '5_clear')
        # клавиша Tab переводит фокус к следующему элементу
        content_login.field_pswd.key_wait_color(
            Keys.TAB,
            field_pswd_css['border_bottom'],
            field_pswd_color['border_bottom'])
        assert not content_login.field_pswd.element_on_focus()
        content_login.field_pswd.screenshot_parent(id, '6_next_focus')
        # клавиша Shift+Tab переводит фокус к предыдущему элементу
        content_login.field_pswd.key_comb(Keys.SHIFT, Keys.TAB)
        # BUG Shift+Tab в Firefox с пароля на кнопку.
        # assert content_login.field_pswd.element_on_focus()
        content_login.field_pswd.screenshot_parent(id, '7_prev_focus')

        # при потере фокуса:
        # исходное состояние
        assert content_login.field_pswd.reset_wait_color(
            field_pswd_css['background'],
            field_pswd_color['background'])
        assert content_login.field_pswd.color(
            field_pswd_css['border_bottom'],
            field_pswd_color['border_bottom'])
        content_login.field_pswd.screenshot(id, '8_no_write')
        # набранные символы замененные на • если введены
        content_login.field_pswd.text(LOGIN_QWERTY[1])
        assert content_login.field_pswd.text_get() == LOGIN_QWERTY[1]
        content_login.field_pswd.screenshot(id, '9_write')

        # Restore
        content_login.field_pswd.key_comb(Keys.CONTROL, Keys.BACKSPACE)
        content_login.field_pswd.reset_wait_color(
            field_pswd_css['border_bottom'],
            field_pswd_color['border_bottom'])

    # TODO добавить скриншоты
    # Button login
        # неактивна
        assert content_login.button_login.attribute('disabled')
        # цвет бледно синий
        assert content_login.button_login.color(
            button_login_css['background'],
            button_login_color['background'])
        # надпись Log in
        assert content_login.button_login.text_get() == 'Log in'
        # цвет надписи белый
        assert content_login.button_login.color(
            button_login_css['text'],
            button_login_color['text'])

        # при наведении:
        # курсор недоступно
        assert content_login.button_login.css('cursor') == 'not-allowed'

        # при нажатии:
        # кнопка вместе с надписью пропорционально уменьшается ~10%
        content_login.button_login.click_hold_wait_transform()

        # при фокусе:
        # click_hold выше, перемещает фокус на элемент.
        # клавиша Shift+Tab переводит фокус к предыдущему элементу
        content_login.button_login.key_comb(Keys.SHIFT, Keys.TAB)
        # BUG Shift+Tab в Firefox проверка бесполезна возможно на будущее \
        # надо проверять не потерю фокуса элементом а фокус на который \
        # элемент перешел
        assert not content_login.button_login.element_on_focus()

        # при клике:
        # изменений не происходит
        content_login.button_login.click()

        # при введенных символах в Username и Password:
        content_login.field_usr.text('q')
        content_login.field_pswd.text('q')
        # активна
        assert content_login.button_login.attribute('disabled') is None
        # курсор pointer
        assert content_login.button_login.css('cursor') == 'pointer'
        # цвет синий
        assert content_login.button_login.color(
            button_login_css['background_activ'],
            button_login_color['background_activ'])

        # при клике неверный логин\пароль:
        content_login.button_login.click()
        # проверка из иконка закрытый замок - при логине
        assert content_login.icon_padlock_flip.is_visible()
        content_login.button_login.click()
        # становится неактивна
        assert content_login.button_login.attribute('disabled')
        # цвет бледно синий
        assert content_login.button_login.color(
            button_login_css['background'],
            button_login_color['background'])
        # FIXME написать проверку ошибки логина
        # при неверных Username и Password всплывающие уведомления
        # столько же сколько было кликов

    # Restore
        # FIXME возможно в будущем тут нужно передать время ожидания
        assert content_login.button_login.color(
            button_login_css['background_activ'],
            button_login_color['background_activ'])
        content_login.field_usr.key(Keys.BACKSPACE)
        content_login.field_pswd.key(Keys.BACKSPACE)
        # TODO добавить ресет действий в action_chains где нужно
        content_login.field_pswd.reset_wait_color(
            field_pswd_css['border_bottom'],
            field_pswd_color['border_bottom'])

        # активируется процесс логина
        # при клике верный логин\пароль:
        content_login.field_usr.text(LOGIN_QWERTY[0])
        content_login.field_pswd.text(LOGIN_QWERTY[1])
        content_login.button_login.click()
        # проверка из иконка закрытый замок - при логине
        # анимация вращения
        assert content_login.icon_padlock_flip.is_visible()
        # иконка сменилась на символ \f13e открытый замок
        # анимация вращения
        assert content_login.icon_padlock_unlock.is_visible()
        # происходит логин
        # перенаправление на:
        assert WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(EC.url_matches(SCHEME + HOST_ADDRES + '/view/dashboard'))
        # в заголовке браузера:
        assert WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(EC.title_is('Dashboard | '+HOST_NAME))

    # Resotre
        # TODO написать разлогин как отдельную функцию за одно и логин
        # TODO добавить скриншотов в весь подтест кейс

    def test_content_login_login_1_3(self):
        id = '1.3'

    # def test_login_page_1_4(self):

    # def test_login_page_1_5(self):

    # def test_(self):
        # self.test_header_1_1()


# TODO разобратся с именами функций для получения текста на кнопке \
# текста введенного в поле, текста вводимого в поле.
# TODO и возможно добавить обертку для прямого доступа к методам и атрибутам
# в принципе надо бы пречисать и стандартизировать имена функций

'''
Отключение анимации в интерфейсе?

diffimg процент и разность нужен простой допилинг и возврат изображения
pixelmatch-py нет процента но есть количество измененных пикселей,
    есть разность, !избежание антиалиасинга и порог срабатывания? чего?

1. Получаем процент разности изображений !возможно не сильно то и легче \
                                            делать отдельно от разности
    если да то строим карту отличий и сохраняем в отчет.

2. Проверяем CSS на изменения !возможно легче чем проверять все скрины \
                                на разность скорее всего зависит от размера \
                                изображения
    если да то строим карту отличий и сохраняем в отчет.

Ускорение проверки интерфейса
скриншот и его проверка занимает много времени
альтернатива скриншоту перед скриншотом проверяем css элемента
если нет изменений считаем что скриншот нет смысла делать.

возможно еще можно получить относительно 00 xy положение элемента
в интерфейсе. !слабо реализуемо и малополезно?
'''
