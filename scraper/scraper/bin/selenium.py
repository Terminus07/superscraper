from seleniumwire import webdriver
from selenium.webdriver import  DesiredCapabilities
from util.dict_util import get_by_key_or_value
from util.func_util import call_func, create_object
from selenium.webdriver.support.ui import Select
from bin.selenium_requests import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType

driver:webdriver.Remote = None
driver_outputs = []

class DriverSettings():
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
    proxy = None
    driver_options = {
        0: "ChromeOptions",
        1: "EdgeOptions",
        2: "FirefoxOptions",
        3: "IeOptions"
    }
    options = {}
    capabilities = {}
    driver_settings = {}
    
    def __init__(self, settings:dict) -> None:
        self.driver_settings = settings
        self.driver_type = self.get_driver_type()
        self.capabilities = self.get_capabilities()
        self.get_proxy()
        self.options = self.get_options()
    
    def get_driver_type(self):
        d = self.driver_settings["driver_type"]
        return d if type(d) is int else get_by_key_or_value(self.driver_types, d)

    def get_options(self):
        driver_options = self.driver_settings['options']
        type = self.driver_options.get(self.driver_type)
        opts =  call_func(webdriver, type, {}) # webdriver.ChromeOptions

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
    
    def get_proxy(self):
        self.proxy = self.driver_settings.get("proxy", None)
        if self.proxy:
            proxy = Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = self.proxy
            proxy.ssl_proxy = self.proxy
            proxy.add_to_capabilities(self.capabilities)
        
    
    def get_options_dict(self):
        capabilities_key = "desired_capabilities" if self.driver_type == 0 else None
        opts_dict = {"options": self.options}
        if capabilities_key:
            opts_dict.update({"desired_capabilities": self.capabilities})

        return opts_dict
  
    
class SeleniumDriver():
    json = {}
    delay = 0 # implicit delay before loading
    events = []
    start_urls = []
    requests = []
    responses = []
    driver_settings:DriverSettings = None
    
    def __init__(self, json) -> None:
       self.json = json
       self.start_urls = json.get('start_urls', [])
       driver_settings = json.get('driver_settings', {})
       self.driver_settings = DriverSettings(driver_settings)
       self.delay = json.get('delay', 0)
       self.events = self.get_events()
       
    def get_driver_instance(self):
        global driver
        if driver is None:
            opts_dict = self.driver_settings.get_options_dict()
            print(opts_dict)
           # equivalent to webdriver.Chrome() and passes arguments as dict
            driver = call_func(webdriver, self.driver_settings.driver_types.get(self.driver_settings.driver_type), opts_dict)
            
        return driver
    
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
  
    def load_urls(self):
        if self.delay > 0: # add implicit wait
            driver.implicitly_wait(self.delay)
        for url in self.start_urls:
            driver.get(url)
    
    def stop_driver(self):
        global driver
        if driver:
            print("DRIVER STOPPED")
            driver.quit()
    
    def handle_events(self):
        for event in self.events:
            event:SeleniumEvent
            event.handle_event()
       
            global driver
            for request in driver.requests:
                self.requests.append(request)
                self.responses.append(request.response)

    def get_html_response(self):
        global driver
        if driver:
            return driver.page_source
    
    def get_current_url(self):
        global driver
        if driver:
            return driver.current_url
    
    def __str__(self):
        print("DRIVER")
        print("TYPE: ", self.driver_settings.driver_type)
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
    delay = 0
    delay_input = None
    
    
    event_types = {
        0: "Target",
        1: "Object",
        2: "Delay"
    }
    
    def __init__(self, index:int,json:dict):
        self.json = json
        self.type = self.get_event_type()
        self.function = json.get('function', None)
        self.target = json.get('target', 'driver')
        self.output = json.get('output', None)
        self.args = json.get('args',None)
        self.object_type = json.get('object_type', None)
        self.object_input = json.get('object_input', None)
        self.delay = json.get('delay', 0)
        self.delay_input = json.get('delay_input', None)
        self.index = index
    
    def get_event_type(self):
        type = 0
        if 'object_type' in self.json:
            type = 1
        if 'delay' in self.json:
            type = 2
        return type
    
    def handle_event(self):
        event_types = {
            0: self.handle_base_event,
            1: self.handle_action_event,
            2: self.handle_delay_event
        }
        
        event_types[self.type]()
    
    def handle_base_event(self):
        self.target = self.get_target()
        output_value = call_func(self.target, self.function, self.args)

        if self.output:
            # store previous outputs
            output = SeleniumOutput(name=self.output, index=self.index,value=output_value)
            driver_outputs.append(output)
    
    def handle_action_event(self):
      
        self.object_input = self.get_output_value(self.object_input, True)
        
        # check if input variable was given
        args = self.object_input.value if self.object_input else self.args
        
        object_instance = create_object(globals(), self.object_type, args)
        object_output = SeleniumOutput(name=self.output, index=self.index, value=object_instance)
        driver_outputs.append(object_output)
    
    def handle_delay_event(self):
        # explicit wait
        print(self)
        wait = WebDriverWait(driver, self.delay)
        function = self.delay_input.get('function')
        args = self.delay_input.get('args')
        try:
            expected_condition = call_func(EC, function, tuple(args))
            element = wait.until(expected_condition)
        except Exception as e:
            print(e)
        print(element)

    
    def get_target(self):
        if 'driver' == self.target: # default value is driver
            return driver
        else:
            target = self.json.get('target')
            return self.get_output_value(target)
            
   
    def get_output_value(self, target, return_object=False):
        try:
            for output in driver_outputs:
                output:SeleniumOutput
                if output.name == target:
                        return output.value if not return_object else output
        except Exception as e:
            print(e)            
    
    
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