### Тестируемый проект
Ajenti2 веб панель администратора сервера.
[GitHub Ajenti2](https://github.com/ajenti/ajenti)

### Основные файлы

#### aвтоматизации:
* `test_autotest.py` (Основной модуль, структурированный для последующего разбития на модули.)
* `screenshots_diff.py` (Модуль сравнения скриншотов запускаемый в отдельном процессе)

#### документации:
* `1.test plan.txt` (Тест план)
* `2.test case.txt` (Шаблон тесткейса)
* `3.test cases.txt` (Тесткейсы)
* `issue` (Баги)


### Использованы инструменты:
* Python
    * lib:
        * pytest
        * selenium.webdriver
        * pixelmatch-py
        * multiprocessing
    * lib вспомогательные:
        * PIL.Image
        * pathlib.Path
        * io.BytesIO
        * time
* Selenium WebDriver

Окружение запускается на KVM в ручную.
> Использован Packer для автосборки образа VM без установки панели. С прицелом авторазвертывания панели и развития до Vagrant
