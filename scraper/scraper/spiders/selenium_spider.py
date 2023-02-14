from spiders.base_spider import BaseSpider
from scraper.bin.selenium import SeleniumDriver
from bin.selenium_requests import *


class SeleniumSpider(BaseSpider):
    name = "selenium"
    json_settings = []
    index = 0
    driver = None
    
    def __init__(self, *args, **kwargs):
        self.json_settings = kwargs
        self.index = self.json_settings.get('index',0)
        super(SeleniumSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        self.driver = SeleniumDriver(self.json_settings)
        self.driver.start_driver()
        self.driver.handle_events()
        self.close(self, 'finished')

    def closed(self, reason):
        self.requests = get_json_requests(self.driver.requests)
        self.responses = get_json_responses(self.driver.responses)
  
        return super().closed(reason)
