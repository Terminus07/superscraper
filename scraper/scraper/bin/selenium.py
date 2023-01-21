from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions, Chrome

class SeleniumHandler():
    driver = None
    driver_types = {
        0: "Chrome",
        1: "Edge",
        2: "Firefox",
        3: "Safari"
    }
    events = []
  
    def __init__(self, events) -> None:
        self.driver = self.get_driver()
        self.events = events
        
    def get_driver(self):
        return self.driver_types.get(0)
   
    def handle_events(self):
        for index,event in enumerate(self.events):
            event = SeleniumEvent(index, self.driver, event['function'])
            print(event)

class SeleniumEvent():
    type = 0
    function = ''
    driver = None
    index = 0
    
    def __init__(self, index:int, driver,function:str):
        self.function = function
        self.driver =  driver
        self.index = index
        
    def __str__(self):
        print("EVENT")
        print("INDEX: ", self.index)
        print("FUNCTION:", self.function)
        print("DRIVER:", self.driver)
        return ""