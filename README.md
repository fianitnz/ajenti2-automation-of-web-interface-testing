### Основные файлы автоматизации:

* `test_autotest.py` (Основной модуль, структурированный для последующего разбития на модули.)
* `screenshots_diff.py` (Модуль сравнения скриншотов запускаемый в отдельном процессе)


`test.py` (Черновик)

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
