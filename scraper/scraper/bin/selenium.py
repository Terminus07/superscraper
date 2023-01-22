from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions, Chrome

driver:webdriver.Remote = None
driver_types = {
    0: "Chrome",
    1: "Edge",
    2: "Firefox",
    3: "Safari"
}

class SeleniumDriver():
    def __init__(self) -> None:
        pass
    
class SeleniumHandler():
    
    events = []
  
    def __init__(self, selenium_json) -> None:
        global driver
        if driver is None:
            driver_type = self.get_driver_type(selenium_json["driver_type"])
            start_driver = getattr(webdriver, driver_type)
            driver = start_driver()
            driver.get("https://www.google.com")
        self.events = selenium_json["events"]
    
    def get_driver_type(self, driver_type):
        return driver_types.get(driver_type) if type(driver_type) is int else driver_type
        
    def handle_events(self):
        for index,event in enumerate(self.events):
            event = SeleniumEvent(index, event['function'])
            print(event)

class SeleniumEvent():
    type = 0
    function = ''
    index = 0
    
    def __init__(self, index:int,function:str):
        self.function = function
        self.index = index
        
    def __str__(self):
        print("EVENT")
        print("INDEX: ", self.index)
        print("FUNCTION:", self.function)
        print("DRIVER:", driver)
        return ""