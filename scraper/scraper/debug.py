from util.file_util import overwrite_json_file,read_json_file
from bin.selenium import SeleniumHandler, SeleniumEvent
# get events json

selenium_json =  read_json_file("json/selenium.json")

handler = SeleniumHandler(selenium_json['events'])
handler.handle_events()
