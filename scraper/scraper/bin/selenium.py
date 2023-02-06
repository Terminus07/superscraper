from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions, IeOptions

from util.dict_util import get_by_key_or_value
from util.func_util import call_func

driver:webdriver.Remote = None
driver_outputs = []

class SeleniumHandler():
    events = []
    selenium_driver = None
    
    def __init__(self, selenium_json) -> None:
        global driver
        self.selenium_driver = SeleniumDriver(selenium_json['driver_settings'], selenium_json['start_urls'])
        self.events = self.get_events(selenium_json["events"])
            
    def get_events(self, events):
        event_items = []
        for index,event in enumerate(events):
            event = SeleniumEvent(index, event)
            event_items.append(event)
        return event_items        
    
    def handle_events(self):
        for event in self.events:
            event:SeleniumEvent
            event.handle_event()

    def start_driver(self):
        global driver
        if driver is None:
            print("DRIVER STARTED")
            driver = self.selenium_driver.get_driver_instance()

    def stop_driver(self):
        global driver
        if driver:
            driver.quit()
    
class SeleniumEvent():
    function = ''
    index = 0
    json = {}
    target = None
    output = None
    args = {}
    
    def __init__(self, index:int,json:dict):
        self.json = json
        self.function = json.get('function', None)
        self.target = json.get('target', 'driver')
        self.output = json.get('output', None)
        self.args = json.get('args',None)
        self.index = index
        
    def handle_event(self):
        self.target = self.get_target()
        output_value = call_func(self.target, self.function, self.args)
    
        if self.output:
            # store previous outputs
            output = SeleniumOutput(name=self.output, index=self.index,value=output_value)
            driver_outputs.append(output)

    def get_target(self):
        if 'driver' == self.target: # default value is driver
            return driver
        else:
            try:
                for output in driver_outputs:
                    output:SeleniumOutput
                    if output.name == self.target:
                        return output.value
            except Exception as e:
                print(e)

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

    options = None
    start_urls = []
    settings = []
    
    def __init__(self, settings, start_urls) -> None:
       self.start_urls = start_urls
       self.settings = settings
       self.driver_type = self.get_driver_type()
       self.options = self.get_options(self.settings['options'])
    
    def get_driver_instance(self):
        global driver
        if driver is None:
           opts_dict = {"options" : self.options} 
           # calls e.g. webdriver.ChromeOptions() and passes options as dict
           driver = call_func(webdriver, self.driver_types.get(self.driver_type), opts_dict)
           driver.get(self.start_urls[0])
        return driver
    
    def get_driver_type(self):
        d = self.settings["driver_type"]
        return d if type(d) is int else get_by_key_or_value(self.driver_types, d)

    def get_options(self, driver_options):
        type = self.driver_options.get(self.driver_type)
        opts =  call_func(webdriver, type, {})
        if 'experimental' in driver_options:
            call_func(opts, "add_experimental_option", driver_options['experimental'])
        return opts
                
    def __str__(self):
        print("DRIVER")
        print("TYPE: ", self.driver_type)
        print("DRIVER:", driver)
        return ""

class SeleniumOutput():
    name:str = ''
    index = 0
    value = ''
    
    def __init__(self, name, index, value) -> None:
        self.name = name
        self.index = index
        self.value = value
        
    def __str__(self):
        print("OUTPUT")
        print("NAME: ", self.name)
        print("VALUE:", self.value)
        return ""