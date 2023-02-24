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


# wget_urls = [
#      "spam-egg",
#      "http://127.0.0.1/asdf/login.php?q=abc#stackoverflow",
#      "https://en.wikipedia.org/wiki/Eiffel_Tower"
# ]
# follow_urls = [
#     "http://127.0.0.1/asdf/login.php?q=abc#stackoverflow"
# ]

# media_urls = [
#     "http://www.example.com/some/path"
# ]

# url_rules = [
        
#         {
#             "target_var": "wget_urls",
#             "function": "search",
#             "args": {
#                 "value": "(?<=-)\w+"
#             }
#         } 
#     ]

# d = { 
#      "wget_urls": wget_urls, 
#     "follow_urls": follow_urls, 
#     "media_urls": media_urls}

# if url_rules:
#     for rule in url_rules:
#         if d.get(rule.get('target_var')):
#             d[rule.get('target_var')] = apply_url_rule( d[rule.get('target_var')], rule)
             
# print(wget_urls, follow_urls, media_urls)

ArgParser.spider({'type': [TEST_DIRECTORY2]})
ArgParser.crawl({})

# download_media([
#     "https://manifest.prod.boltdns.net/manifest/v1/hls/v4/clear/3588749423001/2cb4e463-e7d6-4afc-ac2b-7b3c2984096c/10s/master.m3u8?fastly_token=NjNmODg3Y2ZfMzM3ODY2ODg5MzQwNzFkNGIzMzE1YmNmOThlNTkzZDIwNDc5YzA4MGQxNDdlYTVkNWI3N2IxMWEyMDcxOTc4MQ=="
# ], base_resolution='1080x900')

