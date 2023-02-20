from util.file_util import overwrite_json_file,read_json_file
from bin.selenium import SeleniumDriver, SeleniumEvent, driver_outputs, SeleniumOutput
from util.dict_util import get_by_key_or_value
from selenium.webdriver import  DesiredCapabilities, ChromeOptions, FirefoxOptions, EdgeOptions, IeOptions
from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from util.constants import *
from main import ArgParser
from bin.data_extractor import *
import requests

# DRIVER
# - start urls: List[str]
# - driver_settings: DriverSettings
    # driver_type: int or str
    # options:
    # capabilities:
    # arguments

# EVENT TYPES

# 1) Target event
# - target: str = 'driver'
# - function: str
# - args: dict or list
# - output: Optional[SeleniumOutput] (name, index, value)
    # - name: str (used to point to target value)
    # - index: int (indicates event index in list)
    # - value: str (function to run)
    
# 2) Object event (pass in parameters to an object)
# - object_type: str
# - object_input: Optional[str] (variable previously stored as an output)
# - args: dict or list
# - output: SeleniumOutput

# 3) Delay event (pass in parameters to an object)
# - object_type: str
# - object_input: Optional[str] (variable previously stored as an output)
# - args: dict or list
# - output: SeleniumOutput


# CHAIN SPIDERS

# 1) Generate start urls
#  - If spider index is 0 -> get base urls
#  - else -> if base url is not defined use previous one
# 2) Perform request
# - Request should inherit params from previous response/request (spider_index, type) 
# 3) Check if form data
# 4) Perform form data request
# 5) Save cookie to request/response object
# 6) Start next spider

ArgParser.spider({'type': [GOOGLE_DIRECTORY]})
ArgParser.crawl({})



# opts = webdriver.FirefoxOptions()
# driver = webdriver.Firefox()
# driver.get("https://www.google.com")

 


# selenium_json =  read_json_file(AMAZON_DIRECTORY)
# driver = SeleniumDriver(selenium_json)
# driver.start_driver()
# driver.load_urls()
# driver.handle_events()


# driver = webdriver.Chrome()
# driver.get('https://www.amazon.com')
# element = driver.find_element(by="id", value="nav-link-accountList")
# element.click()


# download_media(["https://manifest.prod.boltdns.net/manifest/v1/hls/v4/clear/3588749423001/a278511c-1765-42a0-bfbf-5f99718f5aa7/10s/master.m3u8?fastly_token=NjNlZjBlMjJfNTIxN2ZiNDViMjViN2RkZTM1ODU4OWNmZjc5NmQ5MWI1YzBmZjA5Y2I2YzIzMGJhZGI4MWI2NDA2NzBmNjU4Zg=="])