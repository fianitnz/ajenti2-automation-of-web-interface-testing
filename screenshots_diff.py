"""
Модуль сравнивающий изображения с эталоном и сохраняющий разность.
Работает в отдельном процессе.
Связь с внешним миром через передачу аргументов , и стек Queue()

создание обекта
pm = PM(win_siz, locale):
    win_siz: разрешение экрана для имени папки
    locale: локаль для имени папки

при инициализации обекта
self.stack = Queue()

глобальная ссылка на стек
STACK = pm.stack

Принимает list
img_b, name, percent = stack.get()
Переписать по нормальному.
"""

from multiprocessing import Process, Queue
from pathlib import Path
import time

from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
from io import BytesIO


class PM():
    def __init__(self, win_siz, locale):
        self.win_siz = win_siz
        self.locale = locale
        self.stack = Queue()

        self.p = Process(target=self._diff, args=(self.stack,))
        self.p.start()

    def _diff(self, stack):
        percent_reciv = 0.0
        time_fix = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime())
        p = Path() / 'screenshots' / self.locale / self.win_siz / time_fix
        # эта проверка лишняя
        # по времени будет создаватся каждый раз уникальный каталог
        if not p.is_dir():
            p.mkdir(parents=True)
        while True:
            img_a, name, percent = stack.get()

            # '_exit' to exit the loop
            if img_a == '_exit':
                break

            img_a = Image.open(BytesIO(img_a))
            img_diff = Image.new('RGBA', img_a.size)
            if percent != 0.0:
                img_b = Image.open(p.joinpath()/'..'/'reference'/(name+'_a.png'))

                mismatch = pixelmatch(img_a, img_b, img_diff)
                percent_reciv = mismatch / (img_a.width * img_a.height) * 100

            if percent_reciv > percent or percent == 0.0:
                img_a.save(p.joinpath()/(name+'_a.png'))
                # Если процент разности 0 не сохраняем.
                # Полученные снимки используем как reference
                if percent > 0.0:
                    img_b.save(p.joinpath()/(name+'_b.png'))
                    img_diff.save(p.joinpath()/(name+'_c.png'))
            print(percent_reciv)
