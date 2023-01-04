from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions, Chrome
from webdriver_manager.chrome import ChromeDriverManager

import sys
import scrapy

class SeleniumSpider():
    name = "selenium"
    
    def __init__(self, *args, **kwargs):
        self.json_settings = kwargs
        
        # get spider controller
        from scraper.main import SpiderController
        self.controller = SpiderController()

        super(SeleniumSpider, self).__init__(*args, **kwargs)
        
    
# initialize driver
s = Service(ChromeDriverManager().install())
opts = ChromeOptions()
opts.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=s, options=opts)
driver.get("https://google.com/")

# find elements
# username = driver.find_element(By.NAME, "_user")
# password = driver.find_element(By.NAME, "_pass")
# dropdown = Select(driver.find_element(By.NAME, "_host"))
# element = driver.find_element(By.ID, "passwd-id")
# element = driver.find_element(By.NAME, "passwd")
# element = driver.find_element(By.XPATH, "//input[@id='passwd-id']")
# element = driver.find_element(By.CSS_SELECTOR, "input#passwd-id")

# events
# element.send_keys()