import os
import io
import csv
import re
import logging
import datetime
import requests
import numpy as np
import pandas as pd
import sys
import time
from urllib.parse import urlencode, urlparse
from bs4 import BeautifulSoup
from datetime import datetime as dt

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import pytesseract
from pytesseract import image_to_string
from PIL import Image


# defining the selenium drivers options #

# url = "https://drt.gov.in/front/page1_advocate.php"

# party_nme = driver.find_element_by_id('').send_keys()
def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    # add the argument and make the browser Headless.
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')
    # For windows
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path="C:/Users/Vipul Kumar/Downloads/chromedriver_win32/chromedriver.exe")
    return driver

def getDetails(driver):
    driver.get("https://drt.gov.in/front/page1_advocate.php")
    # print(res)
    # wait for the element to load
    try:
        WebDriverWait(driver, 5).until(lambda s: s.find_element_by_id("name").is_displayed())
    except TimeoutException:
        print("TimeoutException: Element not found")
        return None
    driver.find_element_by_xpath("//select/option[@value='101']").click()
    element = driver.find_element_by_xpath("//input[@id='name']")
    element.send_keys("sha")
    # driver.find_element_by_xpath("//input[@class='captchatext1']")
    driver.set_window_size(1000, 200)
    element = driver.find_element_by_xpath("//div[@class='captchatext']")  # find part of the page you want image of
    location = element.location
    size = element.size
    driver.save_screenshot('screenshot.png')
    # captcha = driver.find_element_by_xpath('//*[@class="imgcaptcha"]')
    captcha_text = get_captcha_text(location, size)
    captcha_value = int(re.findall(r'[0-9]+',captcha_text)[0])
    captcha = driver.find_element_by_xpath("//input[@class='captchatext1']")
    captcha.send_keys(captcha_value)
    driver.find_element_by_xpath("//input[@id='submit1']").click()

def get_captcha_text(location, size):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    im = Image.open('screenshot.png')  # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save('captcha.png')
    captcha_text = image_to_string(Image.open('screenshot.png'))
    return captcha_text


driver = configure_driver()
getDetails(driver)
# close the driver.
driver.close()



