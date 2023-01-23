from util.file_util import overwrite_json_file,read_json_file
from bin.selenium import SeleniumHandler, SeleniumEvent
from util.dict_util import get_by_key_or_value
from util.func_util import call_func
from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions, IeOptions
from selenium import webdriver

# driver_options = {
#         0: "ChromeOptions",
#         1: "EdgeOptions",
#         2: "FirefoxOptions",
#         3: "IeOptions"
# }



opts = {"name":"detach",
        "value": True}

options = call_func(webdriver, "ChromeOptions")

call_func(options, "add_experimental_option", opts)

options:ChromeOptions
print(options.experimental_options)

# print(get_by_key_or_value(driver_options, 0))

# selenium_json =  read_json_file("json/selenium.json")

# handler = SeleniumHandler(selenium_json)
# handler.get_events()
