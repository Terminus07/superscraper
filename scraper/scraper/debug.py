from util.file_util import overwrite_json_file,read_json_file
from bin.selenium import SeleniumDriver, SeleniumEvent, driver_outputs, SeleniumOutput
from util.dict_util import get_by_key_or_value
from selenium.webdriver import  DesiredCapabilities, ChromeOptions, FirefoxOptions, EdgeOptions, IeOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from json_templates.secret.const import WEBSITE
from selenium.webdriver.support.ui import Select
from util.func_util import create_object
from util.constants import DIRECTORY, OUTPUT_DIRECTORY
from main import ArgParser

# add argument
# experimental option
# executable path
# capabilities

# DRIVER
# - start urls: List[str]
# - driver_settings: dict
    # driver_type: int or str
    # options:
    # capabilities:
    # arguments
    
# EVENT TYPES

# 1) Base event
# - target: str = 'driver'
# - function: str
# - args: dict or list
# - output: Optional[SeleniumOutput] (name, index, value)
    # - name: str (used to point to target value)
    # - index: int (indicates event index in list)
    # - value: str (function to run)
    
# 2) Action event (pass in parameters to an object)
# - object_type: str
# - object_input: Optional[str] (variable previously stored as an output)
# - args: dict or list
# - output: SeleniumOutput

# selenium_json =  read_json_file("{0}/selenium.json".format(DIRECTORY))
# selenium_json['start_urls'] = [WEBSITE]
# driver = SeleniumDriver(selenium_json)
# driver.start_driver()
# driver.handle_events()

argparser = ArgParser()
