from util.file_util import overwrite_json_file,read_json_file
from bin.selenium import SeleniumHandler, SeleniumEvent, driver_outputs, SeleniumOutput
from util.dict_util import get_by_key_or_value
from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions, IeOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# add argument
# experimental option
# executable path
# capabilities

# EVENT TYPES
# 1) Base event
# - driver_type : int or str Optional -> "Chrome"]
# - function 
# - args (dict or list of values) 
# - SeleniumOutput (name, index, value)

# 2) Base event (default)
# 

selenium_json =  read_json_file("json/selenium.json")
handler = SeleniumHandler(selenium_json)
