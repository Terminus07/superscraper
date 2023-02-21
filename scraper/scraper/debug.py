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

# base = 'https://en.wikipedia.org/wiki/Eiffel_Tower'
# r = ['upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg/250px-Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg']
# print(get_relative_link(base, r))

# p = {
#     "titles": [["red", "green", "blue","red"], ["red","red"], ["rega"]],
#     "s": [["re"], ["rega"], ["red", "green", "blue"]],
#     "sas": [["re"], ["rega"], ["red", "green", "blue"]]
# }

# print(os.path.join('images', 'red.js'))


ArgParser.spider({'type': [TEST_DIRECTORY2]})
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


# download_media(["https://manifest.prod.boltdns.net/manifest/v1/hls/v4/clear/3588749423001/a278511c-1765-42a0-bfbf-5f99718f5aa7/10s/master.m3u8?fastly_token=NjNmNTJiMjVfZTU2MzIwNDZlZWViOGYxYjNhMTdiOGUxNTEwYWFlYmQzNTBmOTE1YzEwMjY0NTQ5OTY5MTU4NDE2YmZmNWM1ZA==", 
#                 "https://imdb-video.media-imdb.com/vi1592247065/1434659607842-pgv4ql-1637169338449.mp4?Expires=1677078556&Signature=lfn7SHz5CuACpOnbX0CKnlX1EqvwgSnn98b7pNC-leGSym7knSc9vKzKZzEkwgjn0Tj5FAOz8y3Y5lBkzbzwfaZ82AcKimFpUUNcJKZLF89UstxXImeYtvqclS-oVLLak5HahbRvwFMax7Jn-DXFT1WbCJC5a7Mt9t68yLCNh0SQtsTkK6KYVwyk6Z3mp9w0FIhQhJGq7BNhDdqVJqBA1zdIHVm2VBTYaYeN~0f3nmMCovDgg5J89gM5JTUKbHUOXs6N4PPnI375OdykHY~1MzLWSrdVX~2N7jf8EDCls~CMyxS7SborLeKdzXdPZPAESrVpCX4Koo20t67rz8RWiw__&Key-Pair-Id=APKAIFLZBVQZ24NQH3KA"])