from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions, Chrome

driver:webdriver.Remote = None

class SeleniumHandler():
    events = []
  
    def __init__(self, selenium_json) -> None:
        global driver
        selenium_driver = SeleniumDriver(selenium_json['driver_settings'], selenium_json['start_urls'])
        print(selenium_driver)
        self.events = selenium_json["events"]
            
    def get_events(self):
        for index,event in enumerate(self.events):
            event = SeleniumEvent(index, event['function'])
            self.events[index] = event
            print(self.events)
    
class SeleniumEvent():
    type = 0  
    function = ''
    index = 0
    event_types = {
        0 : "driver",
        1: "object"
    }
    
    def __init__(self, index:int,function:str):
        self.function = function
        self.index = index
 
    def __str__(self):
        print("EVENT")
        print("INDEX: ", self.index)
        print("FUNCTION:", self.function)
        print("DRIVER:", driver)
        return ""

class SeleniumDriver():
    driver_type = 0
    driver_types = {
        0: "Chrome",
        1: "Edge",
        2: "Firefox",
        3: "Safari"
    }
    driver_instance = None
    start_urls = []
    
    def __init__(self, settings, start_urls) -> None:
       self.start_urls = start_urls
       self.driver_type = self.get_driver_type(settings["driver_type"])
       self.driver_instance =  self.get_driver_instance()
       print(self.driver_instance)
       
    def get_driver_type(self, driver_type):
        return self.driver_types.get(driver_type) if type(driver_type) is int else driver_type
    
    def get_driver_instance(self):
        global driver
        if driver is None:
           start = getattr(webdriver, self.driver_type)
           driver = start()
           driver.get(self.start_urls[0])
        return driver
    
    def __str__(self):
        print("DRIVER")
        print("TYPE: ", self.driver_type)
        print("DRIVER:", self.driver_instance)
        return ""