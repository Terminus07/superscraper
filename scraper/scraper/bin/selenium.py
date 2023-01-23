from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.options import BaseOptions, ArgOptions
from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions, IeOptions
from util.dict_util import get_by_key_or_value

driver:webdriver.Remote = None

class SeleniumHandler():
    events = []
    seleniumDriver = None
    previous_event = None
    next_event = None
    
    def __init__(self, selenium_json) -> None:
        global driver
        self.selenium_driver = SeleniumDriver(selenium_json['driver_settings'], selenium_json['start_urls'])
        self.events = selenium_json["events"]
            
    def get_events(self):
        for index,event in enumerate(self.events):
            event = SeleniumEvent(index, event['function'])
            self.events[index] = event        
    
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
     
    def handle_event(self):
        print(self.function)
    
    def __str__(self):
        print("EVENT")
        print("INDEX: ", self.index)
        print("FUNCTION:", self.function)
        print("DRIVER:", driver)
        return ""

class SeleniumDriver():
    driver_type = 0 # always integer
    
    driver_types = {
        0: "Chrome",
        1: "Edge",
        2: "Firefox",
        3: "Safari"
    }
    
    driver_options = {
        0: "ChromeOptions",
        1: "EdgeOptions",
        2: "FirefoxOptions",
        3: "IeOptions"
    }

    driver_instance = None
    start_urls = []
    options = []
    settings = []
    
    
    def __init__(self, settings, start_urls) -> None:
       self.start_urls = start_urls
       self.settings = settings
       self.driver_type = self.get_driver_type()
       self.driver_instance =  self.get_driver_instance()
       self.options = self.get_options()
  
    def get_driver_instance(self):
        global driver
        if driver is None:
           start = getattr(webdriver, self.driver_types.get(self.driver_type))
           driver = start()
           driver.get(self.start_urls[0])
        return driver
    
    def get_driver_type(self):
        d = self.settings["driver_type"]
        return d if type(d) is int else get_by_key_or_value(self.driver_types, d)

    def get_options(self):
        type = self.driver_options.get(self.driver_type)
        opts = getattr(webdriver, type)
        options = opts()
        return options
                
    def __str__(self):
        print("DRIVER")
        print("TYPE: ", self.driver_type)
        print("DRIVER:", self.driver_instance)
        return ""