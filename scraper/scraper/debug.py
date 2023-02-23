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
from urllib.parse import urlparse,urlsplit, urlunsplit


 
# urls = [
#      "http://www.example.com/some/path",
#      "http://127.0.0.1/asdf/login.php?q=abc#stackoverflow",
#      "https://en.wikipedia.org/wiki/Eiffel_Tower"
#       
    
# ]

# for url in urls:
#     split_url = urlsplit(url)
#     clean_path = "".join(url.split(split_url.path)[0]) if split_url.path else url
#     print(clean_path)
    

ArgParser.spider({'type': [TEST_DIRECTORY2]})
ArgParser.crawl({})

# download_media([
#     "https://manifest.prod.boltdns.net/manifest/v1/hls/v4/clear/3588749423001/fcab68b1-23f0-4d78-b2e3-19b09e473e6e/10s/master.m3u8?fastly_token=NjNmODAyOTNfZDFlZWRlY2Y2NmU1MDRkYWQwZjJkMjRmMjhhYTQ4YjQ3YjI1NTdhMTQwMjVjNWQ2MTJhMTI0NWM3MTFmOWNhOA=="
# ])
