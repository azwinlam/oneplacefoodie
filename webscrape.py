from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import requests
from bs4 import BeautifulSoup

import time

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='C:\webdrivers\chromedriver.exe',options=chrome_options) # to open the chromebrowser 
driver.get("https://www.openrice.com/zh/hongkong/restaurants?districtId=1999&districtId=2999&districtId=3999")
actions = ActionChains(driver)


links = True
page_count = 1
#find all the restaurant links on the page

while links == True:
    restaurant_urls = []
    restaurants = driver.find_elements_by_xpath('//h2[@class="title-name"]/a')
    time.sleep(0.1)
    for restaurant in restaurants:
        restaurant_urls.append(restaurant.get_attribute("href"))
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="pagination-button next js-next"]')))
        next_pg = driver.find_element_by_xpath('//a[@class="pagination-button next js-next"]')
        next_pg.location_once_scrolled_into_view
        time.sleep(0.5)
        next_pg = driver.find_element_by_xpath('//a[@class="pagination-button next js-next"]')
        next_pg.click()
        page_count += 1
        print(f"Page Count : {page_count}")
        with open("open_rice_urls.txt","a")as f:
            for url in restaurant_urls:
                f.write("%s\n" % url)
    except:
        links = False


print("Complete")


