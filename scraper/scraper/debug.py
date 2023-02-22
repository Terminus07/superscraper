from util.file_util import overwrite_json_file,read_json_file
from bin.selenium import SeleniumDriver, SeleniumEvent, driver_outputs, SeleniumOutput
from util.dict_util import get_by_key_or_value
from selenium.webdriver import  DesiredCapabilities, ChromeOptions, FirefoxOptions, EdgeOptions, IeOptions
# from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from util.constants import *
from main import ArgParser
from bin.data_extractor import *
import requests

# ArgParser.spider({'type': [IMDB_DIRECTORY]})
# ArgParser.crawl({})

# opts = webdriver.FirefoxOptions()
# driver = webdriver.Firefox()
# driver.get("https://www.google.com")

# selenium_json =  read_json_file(IMDB_DIRECTORY)
# driver = SeleniumDriver(selenium_json)
# driver.start_driver()
# driver.load_urls()
# driver.handle_events()


# driver = webdriver.Chrome()
# driver.get('https://www.amazon.com')
# element = driver.find_element(by="id", value="nav-link-accountList")
# element.click()


# download_media([])