from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import  DesiredCapabilities, ChromeOptions, FirefoxOptions, EdgeOptions, IeOptions

from util.dict_util import get_by_key_or_value
from util.func_util import call_func

driver:webdriver.Remote = None
driver_outputs = []

class SeleniumDriver():
    json = {}
    
    driver_type = 0 # always integer
    
    driver_types = {
        0: "Chrome",
        1: "Edge",
        2: "Firefox",
        3: "Safari"
    }
    
    driver_capabilities = {
        0: DesiredCapabilities.CHROME,
        1: DesiredCapabilities.EDGE,
        2: DesiredCapabilities.FIREFOX,
        3: DesiredCapabilities.SAFARI
    }
    
    driver_options = {
        0: "ChromeOptions",
        1: "EdgeOptions",
        2: "FirefoxOptions",
        3: "IeOptions"
    }
    events = []
    options = None
    capabilities = None
    start_urls = []
    driver_settings = []
    
    def __init__(self, json) -> None:
       self.json = json
       self.start_urls = json.get('start_urls', [])
       self.driver_settings = json.get('driver_settings', {})
       self.events = self.get_events()
       self.driver_type = self.get_driver_type()
       self.options = self.get_options()
       self.capabilities = self.get_capabilities()
 
    def get_driver_instance(self):
        global driver
        if driver is None:
           opts_dict = {"options" : self.options, "desired_capabilities": self.capabilities} 
        
           # equivalent to webdriver.Chrome() and passes arguments as dict
           driver = call_func(webdriver, self.driver_types.get(self.driver_type), opts_dict)
           driver.get(self.start_urls[0])
        return driver
    
    def get_driver_type(self):
        d = self.driver_settings["driver_type"]
        return d if type(d) is int else get_by_key_or_value(self.driver_types, d)

    def get_options(self):
        driver_options = self.driver_settings['options']
        type = self.driver_options.get(self.driver_type)
        opts =  call_func(webdriver, type, {})
        
        # generate experimental_options
        experimental_options = driver_options.get('experimental_options', [])
        for opt in experimental_options:
            call_func(opts, "add_experimental_option", opt)
        
        # generate arguments
        arguments  = driver_options.get('arguments', [])
        for arg in arguments:
            call_func(opts, "add_argument", arg)
  
        return opts
    
    def get_capabilities(self):
        capabilities = self.driver_settings.get('capabilities', {})
        capabilities_type = self.driver_capabilities.get(self.driver_type)
        capabilities.update(capabilities_type)
        return capabilities
  
    def get_events(self):
        events = self.json.get('events',[])
        for index,event in enumerate(events):
            event = SeleniumEvent(index, event)
            self.events.append(event)
        return self.events
    
    def start_driver(self):
        global driver
        if driver is None:
            print("DRIVER STARTED")
            driver = self.get_driver_instance()

    def stop_driver(self):
        global driver
        if driver:
            driver.quit()
    
    def handle_events(self):
        for event in self.events:
            event:SeleniumEvent
            event.handle_event()
    
                 
    def __str__(self):
        print("DRIVER")
        print("TYPE: ", self.driver_type)
        print("DRIVER:", driver)
        return ""
    
class SeleniumEvent():
    function = ''
    index = 0
    json = {}
    target = None
    output = None
    args = {}
    type = 0
    object_type = None
    object_input = None
    
    event_types ={
        0: "Base",
        1: "Action"
    }
    
    def __init__(self, index:int,json:dict):
        self.json = json
        self.type = 1 if 'object_type' in self.json else 0 
        self.function = json.get('function', None)
        self.target = json.get('target', 'driver')
        self.output = json.get('output', None)
        self.args = json.get('args',None)
        self.object_type = self.get_object_type()
        self.object_input = self.get_object_type()
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
            self.get_output_value(self.target)
    
    def get_output_value(self, target):
        try:
            for output in driver_outputs:
                output:SeleniumOutput
                if output.name == target:
                    return output.value
        except Exception as e:
            print(e)            
    
    def get_object_type(self):
        if self.type == 1:
            pass
    
    def get_object_input(self):
        return self.get_output_value(self.json.get('object_input', None))
        

    def __str__(self):
        print("EVENT")
        print("TYPE:", self.event_types.get(self.type))
        print("INDEX: ", self.index)
        print("FUNCTION:", self.function)
        print("TARGET:", self.target)
        print("OUTPUT:", self.output)
        print("DRIVER:", driver)
        print("OBJECT_INPUT:", self.object_input)
        print("OBJECT_TYPE:", self.object_type)
       
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