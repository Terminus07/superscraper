import scrapy
import os, signal
from spiders.base_spider import BaseSpider
from scraper.bin.selenium import SeleniumDriver
from util.dict_util import update_dict

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
        driver = SeleniumDriver(self.json_settings)
        driver.start_driver()
        driver.handle_events()
        self.close(self, 'finished')

    
    def closed(self, reason):
        print('HELLO')
        return super().closed(reason)
