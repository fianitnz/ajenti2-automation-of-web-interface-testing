'''import pytest

from PIL import Image, ImageDraw
from selenium import webdriver
import os
import sys

class ScreenAnalysis:

    STAGING_URL = 'http://www.yahoo.com'
    PRODUCTION_URL = 'http://www.yahoo.com'
    driver = None

    def __init__(self):
        self.set_up()
        self.capture_screens()
        self.analyze()
        self.clean_up()

    def set_up(self):
        self.driver = webdriver.Firefox(executable_path='../selenium/geckodriver')
        #self.driver = webdriver.phantomjs()

    def clean_up(self):
        self.driver.close()

    def capture_screens(self):
        self.screenshot(self.STAGING_URL, 'screen_staging.png')
        self.screenshot(self.PRODUCTION_URL, 'screen_production.png')

    def screenshot(self, url, file_name):
        print("Capturing", url, "screenshot as", file_name, "...")
        self.driver.get(url)
        self.driver.set_window_size(1024, 768)
        self.driver.save_screenshot(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'screenshots', file_name))
        self.driver.get_screenshot_as_png()
        self.driver.get_screenshot_as_file(file_name)
        print("Done.")

    def analyze(self):
        screenshot_staging = Image.open("screen_staging.png")
        screenshot_production = Image.open("screen_production.png")
        columns = 60
        rows = 80
        screen_width, screen_height = screenshot_staging.size

        block_width = ((screen_width - 1) // columns) + 1 # this is just a division ceiling
        block_height = ((screen_height - 1) // rows) + 1

        for y in range(0, screen_height, block_height+1):
            for x in range(0, screen_width, block_width+1):
                region_staging = self.process_region(screenshot_staging, x, y, block_width, block_height)
                region_production = self.process_region(screenshot_production, x, y, block_width, block_height)

                if region_staging is not None and region_production is not None and region_production != region_staging:
                    draw = ImageDraw.Draw(screenshot_staging)
                    draw.rectangle((x, y, x+block_width, y+block_height), outline = "red")

        screenshot_staging.save("result.png")

    def process_region(self, image, x, y, width, height):
        region_total = 0

        # This can be used as the sensitivity factor, the larger it is the less sensitive the comparison
        factor = 100

        for coordinateY in range(y, y+height):
            for coordinateX in range(x, x+width):
                try:
                    pixel = image.getpixel((coordinateX, coordinateY))
                    region_total += sum(pixel)/4
                except:
                    return

        return region_total/factor

ScreenAnalysis()
'''
'''
from multiprocessing import Process, Queue, Manager
import time

def a(b, c):
    bb = b.get()
    while True:
        print(c.get())
        time.sleep(3)

b = Queue()
c = Queue()
b.put(True)
c.put([0, 1, 2])

p = Process(target=a, args=(b, c))
p.start()
time.sleep(6)
p.terminate()
'''
from multiprocessing import Process, Queue, Value
import time

from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch

#class MP():
    #def diff(self, stack):
        #while True:
            #print('_diff is run')
            #self.one = stack.get()
            #print(self.one)
            #if self.one == '_exit':
                #print('break')
                #break
            ##img_b, folder, name = stack.get()

            #img_a = Image.open("a.png")
            #img_b = Image.open("b.png")
            #img_diff = Image.new("RGBA", img_a.size)

            #mismatch = pixelmatch(img_a, img_b, img_diff)
            #time.sleep(5)
            #img_diff.save("c.png")
            #print('img_diff.save')
        ##return (mismatch / (img_a.width * img_a.height)) * 100

    #def start(self):
        #self.stack = Queue()
        ##self.one = None

        #self.p = Process(target=self.diff, args=(self.stack,))
        #self.p.start()

I = 1
mismatch = None
def a():
    global I
    while I == 1:
        print('_diff is run')
        #one, two, three, four = stack.get()
        #time.sleep(5)
        if I == 0:
            print('break')
            break
        #img_b, folder, name = stack.get()

        img_a = Image.open("a.png")
        img_b = Image.open("b.png")
        img_diff = Image.new("RGBA", img_a.size)

        mismatch = pixelmatch(img_a, img_b, img_diff)
        img_diff.save("c.png")
        print('img_diff.save')
        print(mismatch)
    return (mismatch / (img_a.width * img_a.height)) * 100




