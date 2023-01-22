from util.file_util import overwrite_json_file,read_json_file
from bin.selenium import SeleniumHandler, SeleniumEvent
from util.dict_util import get_by_key_or_value

# driver_options = {
#         0: "ChromeOptions",
#         1: "EdgeOptions",
#         2: "FirefoxOptions",
#         3: "IeOptions"
# }

# print(get_by_key_or_value(driver_options, 0))

selenium_json =  read_json_file("json/selenium.json")

handler = SeleniumHandler(selenium_json)
handler.get_events()
