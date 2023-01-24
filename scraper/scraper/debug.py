from util.file_util import overwrite_json_file,read_json_file
from bin.selenium import SeleniumHandler, SeleniumEvent, driver_outputs, SeleniumOutput
from util.dict_util import get_by_key_or_value
from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions, IeOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# driver_options = {
#         0: "ChromeOptions",
#         1: "EdgeOptions",
#         2: "FirefoxOptions",
#         3: "IeOptions"
# }

# add argument
# experimental option
# executable path
# capabilities

# element = handler.selenium_driver.driver_instance.find_element("gsc-i-id2")
# element.send_keys(Keys.Re)
selenium_json =  read_json_file("json/selenium.json")
handler = SeleniumHandler(selenium_json)

handler.handle_events()
for d in driver_outputs:
    d:SeleniumOutput
    print(d)