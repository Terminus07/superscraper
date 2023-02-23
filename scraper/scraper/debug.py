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

# from urllib.parse import 
# ArgParser.spider({'type': [PORT_DIRECTORY]})
# ArgParser.crawl({})

# print( "https://fores.web.ua.pt/wp-content/uploads/2022/06/EEA_grants@4x.png" ==   
#       "https://fores.web.ua.pt/wp-content/uploads/2022/06/EEA_grants@4x.png")

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
# download_media(["https://manifest.prod.boltdns.net/manifest/v1/hls/v4/clear/3588749423001/f88b79a8-9ab4-4c22-aa61-770bba024bb7/10s/master.m3u8?fastly_token=NjNmNmVjNTVfOGZlYmUyMmY0YTZlZThiNzI4MmEwNmI5ODk5MDQ3MDU1ZTBmZjUyMmY2ZTI1MTI0NWZjOTg2ZDM0ZmEzNzhlZA=="])

download_media([
    "https://house-fastly-signed-eu-west-1-prod.brightcovecdn.com/media/v1/hls/v4/clear/3588749423001/a278511c-1765-42a0-bfbf-5f99718f5aa7/bbb59805-4f2b-494b-9b7f-ca8a8168b9cc/5x/segment23.ts?fastly_token=NjNmNmVmMTRfZGExY2VkNzE5YWUzNzg0NDg1YTljZTE2OTYxYjA4MDFkNjQwNjg3ZmNjNTNlNzBlMDdmMjVlNmIzN2I3ZTM3Ml8vL2hvdXNlLWZhc3RseS1zaWduZWQtZXUtd2VzdC0xLXByb2QuYnJpZ2h0Y292ZWNkbi5jb20vbWVkaWEvdjEvaGxzL3Y0L2NsZWFyLzM1ODg3NDk0MjMwMDEvYTI3ODUxMWMtMTc2NS00MmEwLWJmYmYtNWY5OTcxOGY1YWE3L2JiYjU5ODA1LTRmMmItNDk0Yi05YjdmLWNhOGE4MTY4YjljYy8="
])