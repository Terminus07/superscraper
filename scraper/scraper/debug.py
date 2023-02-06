from util.file_util import overwrite_json_file,read_json_file
from bin.selenium import SeleniumHandler, SeleniumEvent, driver_outputs, SeleniumOutput
from util.dict_util import get_by_key_or_value
from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions, IeOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from json_templates.secret.const import WEBSITE
# add argument
# experimental option
# executable path
# capabilities

# EVENT TYPES

# 1) Base event
# - target: str = 'driver' (execute default driver)
# - function: str 
# - args: dict or list
# - output: Optional[SeleniumOutput] (name, index, value)
    # - name: str (used to point to target value)
    # - index: int (indicates event index in list)
    # - value: str (function to run)
    
# 2) Regular event
# 

selenium_json =  read_json_file("json_templates/selenium.json")
selenium_json['start_urls'] = [WEBSITE]
print(selenium_json)
# handler = SeleniumHandler(selenium_json)

# handler.start_driver()
# handler.handle_events()