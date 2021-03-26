# #############################################################################
#
#
#
# #############################################################################
class LocatorsHeader():
    pass


class Header(LocatorsHeader):
    pass


@pytest.fixture(scope='module', autouse=True)
def InitWebDriver():
    a = '\no lo lo'
    yield a
    import time
    time.sleep(2)
    print('\nquit', a)


class TestCase():
    def test_test(self, InitWebDriver):
        self.a = InitWebDriver
        #assert False
        print(self.a)
        assert True
    def test_test2(self, InitWebDriver):
        self.a = InitWebDriver
        #assert False
        print(self.a)
        assert True


# #############################################################################
#
#
#
# #############################################################################
class LocatorsHeader():
    def __init__(self):
        self.header = DRIVER.find()
    def link_ajenti(self):
        return header.find()
    def host_name(self):
        pass
    def resize(self):
        pass


class Link():
    def __init__(self, locator):
        self.text = ''
    def clic(self):
        pass
    def screenshot_no_mouse(self):
        pass
    def screenshot_on_mouse(self):
        pass


class Header():
    locators = LocatorsHeader()
    link_ajenti = Link(locators.link_ajenti())


class TestCase1():
    header = Header()
    assert header.link_ajenti.text
    header.link_ajenti.clic()
    assert DRIVER.current_url == ''


# #############################################################################
#
#
#
# #############################################################################
class wait_color_loc_elm():
    def wait_color


class Screenshot():
    def take_screenshot(self, subname):
        DRIVER \
            .find_element(*self.locator) \
            .screenshot('header_{}x{}_{}.png'.format(*WINDOW_SIZE, subname))


class LocatorsHeader():
    header = (By.XPATH, '//nav')
    link_ajenti = (By.XPATH, '//nav//a[contains(., "Ajenti")]')
    link_ajenti_css = {'background': 'border-left-color'}
    link_ajenti_color = {'background': 'rgba(207, 207, 207, 1)'}

class Locators():
    body = (By.TAG_NAME, 'BODY')


class Link(Screenshot):
    def __init__(self, locator):
        self.locator

    def get_text(self):
        return DRIVER.find_element(*self.locator).text

    def link_adders(self):
        return DRIVER.find_element(*self.locator).get_attribute('href'))

    def mouse_on_wiat_color(self, locat, css, color):

        wait_color_loc_elm(loc_or_elm, css, color)

    def click_hold_wiat_color(self, locat, css, color):

        wait_color_loc_elm(loc_or_elm, css, color)

    def click(self):
        DRIVER.find_element(*self.locator).clic()


class Header(Screenshot):
    prefix = 'header'
    suffix = 'header'
    locator = LocatorsHeader.header
    locator_body = Locators.body

    link_ajenti = Link(LocatorsHeader.link_ajenti)


class Test():
    header = Header()
    header.link_ajenti.click()
