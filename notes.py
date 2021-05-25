import pytest

pytest --tb=auto -v -s test_autotest.py

--tb= трассировка ошибки (auto/long/short/line/native/no)
--tb=auto
--tb=line в одну строку

-v больше отладочной информации, вывод названия текущего теста

--capture=no stdout/stderr отключить запись, выводить в консоль
-s —


# #############################################################################
#
#
#
# #############################################################################
def setup():
    print('\n-------', "setup()", '-------')

def teardown():
    print('\n-------', "teardown()", '-------')

def setup_module(module):
    print('\n.......', "setup_module()", '.......')

def teardown_module(module):
    print('\n.......', "teardown_module()", '.......')

def setup_function(function):
    print('\n=======', "setup_function()", '=======')

def teardown_function(function):
    print('\n=======', "teardown_function()", '=======')


def test_numbers_3_4():
    print("test_numbers_3_4()")
    assert 3*4 == 12

def test_strings_a_3():
    print("test_strings_a_3()")
    assert 'a'*3 == 'aaa'

class TestUM:
    def setup(self):
        print ("\n*///setup///*")

    def teardown(self):
        print ("\n*///teardown///*")

    def setup_class(cls):
        print ("\n*---setup_class---*")

    def teardown_class(cls):
        print ("\n*---teardown_class---*")

    def setup_method(self, method):
        print ("\n*+++setup_method+++*")

    def teardown_method(self, method):
        print ("\n*+++teardown_method+++*")

    def test_numbers_5_6(self):
        print ("\ntest 5*6")
        assert 5*6 == 30

    def test_strings_b_2(self):
        print ("\ntest b*2")
        assert 'b'*2 == 'bb'


# #############################################################################
#
#
#
# #############################################################################
# Пропуск теста
@pytest.mark.skip('skip test open panel')

# Фикстура позволяющая запускать тест с разными параметрами
@pytest.mark.parametrize

# #############################################################################
#
#
#
# #############################################################################
# Передача в класс как параметра глобального обеката браузера, не имеет смысла
# так как кто это будет делать, ...если только попробвать через функцию
#                                                     инициализации или фикстуру


# Неработает __init__ в тестовом классе __init__ нужен pytest для внутренней
#                                                                         работы
# Ошибка: PytestCollectionWarning

# class TestClass():
#     def __init__(self):
#         pass
#     def test_metod():
#         pass


# Неработает __init__ в родительском классе
# Ошибка: metaclass
# что то не воспроизводится ошибка, хз как я это сделал и так и так пробую...

class Init():
    def __init__(self):
        pass

class TestClass(Init):
    def test_metod(self):
        pass

    #1 инициализируем обект внешний класс внутри тестового который \
#делает __init__ нужного нам обекта и через суб обект получаем доступ.

    #2 создаем в тестовом классе метод который который будет создавтаь нужное \
#окружение в текущем классе и вызываем его в первом тестовом методе перед \
#продолжением теста.

    #3 используем встроенный в pytest декоратор подготавливающий среду для \
#тестирования.

# фикстуры или сетап теардовн он же xunit метод

#__init_subclass__??

#Проверить переприсвоение переменной внутри класса возможно будет работать в созданном объекте так как в методе обекта нет доступа к глобальной переменной даже если принудительно указать глобал, хотя при создании обекта можно из класса вывести принт с глобальной переменной


# Page load timeout.
# Assertion о возбужденном исключении,
# если не возбуждено ошибка Failed: DID NOT RAISE .
from selenium.common.exceptions import TimeoutException
DRIVER.set_page_load_timeout(1)
with pytest.raises(TimeoutException) as error:
    DRIVER.get(SCHEME + HOST_ADDRES)
assert 'TimeoutException' in error.value

        '''Прикольная фишка как получить исходник элемента. Перенести в note.
        print(self.ajenti.get_attribute('innerHTML'))
        '''

https://extendsclass.com/xpath-tester.html
http://videlibri.sourceforge.net/cgi-bin/xidelcgi

//*[contains(text(), 'Ajenti')]/..
//a[contains(*, 'Ajenti')]
//nav[contains(a,'')]
//nav/descendant::*[contains(text(), 'Aj')]
//nav/div/p[contains(., 'qwerty')]

//nav/descendant::a[contains(., 'Ajenti')]
//nav/descendant::p[contains(., 'qwerty')]
//nav/descendant::a[@click='toggleWidescreen()']

//nav/descendant::a[contains(normalize-space(@click), 'toggleWidescreen')]
//nav//a[contains(normalize-space(@click), 'toggleWidescreen')]
//nav//a[contains(@*, 'toggleWidescreen()')]
//nav//a[@*='toggleWidescreen()']

https://medium.com/nuances-of-programming/python-статические-методы-методы-класса-и-экземпляра-класса-3e8529d24786
@staticmethod — используется для создания метода, который ничего не знает о классе или экземпляре, через который он был вызван. Он просто получает переданные аргументы, без неявного первого аргумента, и его определение неизменяемо через наследование.

Проще говоря, @staticmethod — это вроде обычной функции, определенной внутри класса, которая не имеет доступа к экземпляру, поэтому ее можно вызывать без создания экземпляра класса.

@classmethod — это метод, который получает класс в качестве неявного первого аргумента, точно так же, как обычный метод экземпляра получает экземпляр. Это означает, что вы можете использовать класс и его свойства внутри этого метода, а не конкретного экземпляра.

Проще говоря, @classmethod — это обычный метод класса, имеющий доступ ко всем атрибутам класса, через который он был вызван. Следовательно, classmethod — это метод, который привязан к классу, а не к экземпляру класса.

###############################################################################
#
#
#
###############################################################################

import time
st_time1 = time.time()
print(time.time() - st_time1, 'time1')

#print(dir())
for i in dir():
    print(i, sep = '\n')
print('==================')
for i in globals():
    print(i, sep = '\n')
print('==================')
for i in locals():
    print(i, sep = '\n')
print('==================')

#print(list(locals())

###############################################################################
#
#
#
###############################################################################
# Проверка исключения
with pytest.raises(ZeroDivisionError):

# Изменяемый локатор
@classmethod # Это лишнее
def PHRASE_RESULTS(cls, phrase):
    xpath = f"//div[@id='links']//*[contains(text(), '{phrase}')]"
    return (By.XPATH, xpath)

# #############################################################################
#
#
#
# #############################################################################
# For "Explicit Wait" while working "Implicit Wait"
class a():
    def __enter__(self):
        print('a1')
    def __exit__(self, exc_type = None, exc_value = None, traceback = None):
        print('a2')
b = a()

with b:
    print('ololo')
>>a1
>>ololo
>>a2


# #############################################################################
#
# Modules
#
# #############################################################################
class Screenshot():
    def take_screenshot(self, subname):
        WebDriverWait(DRIVER, DEFAULT_TIME) \
            .until(EC.visibility_of_element_located(self.locator)) \ # локатор распаковывается внутри
            .screenshot('header_{}x{}_{}.png'.format(*WINDOW_SIZE, subname))
        '''
        DRIVER \
            .find_element(*self.locator) \
            .screenshot('header_{}x{}_{}.png'.format(*WINDOW_SIZE, subname))'''


# #############################################################################
#
# Tests
#
# #############################################################################
DRIVER.implicitly_wait(4)


class ImplicitlyWaitPause():
    def __enter__(self):
        DRIVER.implicitly_wait(0)

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        DRIVER.implicitly_wait(4)


implicitly_wait_pause = ImplicitlyWaitPause()

        # Попытка сделать отключение implicitly_wait
        # Но то ли его можно уже использовать с WebDriverWait
        # И рекомендация не смешивать устарела.
        # Или эта ошибка плавающая. Суммирования времени не произошло.
        # Реализованно три разных подхода к проверке заголовка.
        # Первые два с ожиданием появления элемента.
        # Третий был реализацией с time.sleep сейчас бесполезен.
        with implicitly_wait_pause:
            assert WebDriverWait(DRIVER, DEFAULT_TIME) \
                .until(EC.title_is(HOST_NAME))
        assert DRIVER.find_element(By.TAG_NAME, 'title') \
            .get_property('text') == HOST_NAME
        assert DRIVER.title == HOST_NAME
# #############################################################################
#
#
#
# #############################################################################
    def no_mouse(self):
        element = DRIVER.find_element(*LocatorsHeader.link_ajenti)
        ActionChains(DRIVER) \
            .move_to_element_with_offset(element,
                                         element.size[],
                                         element.size[]) \
            .perform()
        ActionChains(DRIVER) \
            .move_to_element(DRIVER.find_element(*LocatorsHeader.link_ajenti)) \
            .perform()
        ActionChains(DRIVER) \
            .move_to_element_with_offset(elmnt,
                                         elmnt.size['width']+10,
                                         elmnt.size['height']+10)
            .perform()


# #############################################################################
#
#
#
# #############################################################################
        assert DRIVER.find_element(By.TAG_NAME, 'title') \
            .get_property('text') == HOST_NAME, name
        assert DRIVER.title == HOST_NAME, name


# #############################################################################
#
#
#
# #############################################################################



# #############################################################################
#
#
#
# #############################################################################



# #############################################################################
#
#
#
# #############################################################################



# #############################################################################
#
# Chrome
#
# #############################################################################
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
browser = webdriver.Chrome(executable_path = path_to_chromedriver,chrome_options=chrome_options)


https://help.applitools.com/hc/en-us/articles/360007189411--Chrome-is-being-controlled-by-automated-test-software-notification

chrome_options = webdriver.ChromeOptions();
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
driver = webdriver.Chrome(options=chrome_options);

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
caps = options.to_capabilities()
driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                            desired_capabilities=caps)
# #############################################################################
#
#
#
# #############################################################################
    Как автоматизатор, я хочу описать взаимодействие со всеми элементами в приложении один раз и больше не задумываться о том, как это работает

Ниже разговор уже пойдет о фреймворках так или иначе касающихся взаимодействия с UI-частью приложения через Selenium. И здесь уже не о библиотеке, а о стандартном подходе в Page Object Model, где в каждом из проектов описываются следующие пакеты/модули:

    elements (взаимодействие с кнопками/инпутами и любыми другими элементами, доступными в приложении. Здесь вам и ожидания и логирование и обработка исключения)
    pages - описание локаторов и действий с каждым из элементов, используя классы из elements
    steps - объединение отдельных действий из разных страниц в так называемые business-scenarios, имеющих ценность для конечного пользователя/описываемые в репортинге. Создатели Serenity прекрасно переиспользовали такую модель у себя во фреймворке, но, к сожалению, пожертвов определенной гибкостью
    tests - из отдельных шагов собирается тестовый сценарий, из тестов только пробрасывается ввод от конечного пользователя

Итак, элементы расписаны, из них составляем страницы, из страниц составляем наборы бизнес-шагов, из них тестовые сценарии.



# #############################################################################
#
#
#
# #############################################################################

Библиотеки python для работы с изображениями
    scikit-image
    numpy
    scipy
    pillow
    opencv

pixel perfect наложение макета на скриншот страницы
page ruller тестирование разметки(расстояние мужду блоков в ручную)
what front проверка шрифтов, лицензирования
spellchecker орфография
window resizer адаптируемость страницы
появление\исчезновение курсора при наведении на элементы
появление курсора и вводимых символов в полях ввода
проверка стандартов w3c html, css


https://userium.com
https://www.checkmycolours.com
https://goo.gl/SbGz5v
https://checkvist.com/checklists/476089






