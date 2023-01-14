from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions, Chrome

class SeleniumHandler():
    driver_type = None
    driver = None
    
    def __init__(self, driver_type) -> None:
        self.driver_type = driver_type
    
    def get_driver(self, index):
        print("INDEX", index)
        

    def handle_events(self, events):
        for event in events:
            print(event)
            
class SeleniumEvent():
    type = 0
    function = ''
    driver = None
    
    def __init__(self, driver_type, event_json):
        pass