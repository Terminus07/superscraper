from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions, FirefoxOptions, Chrome
from webdriver_manager.chrome import ChromeDriverManager

import scrapy
import os
import signal

class SeleniumSpider(scrapy.Spider):
    name = "selenium"
    
    driver_type = 0
    json_settings = []
    index = 0
    request = {}
    response = {}
    
    options = []
    driver = None
    handler = None
    driver_type = None
    events = []
    
    def __init__(self, *args, **kwargs):
        self.json_settings = kwargs
        self.index = kwargs['index']

        # get spider controller
        from scraper.bin.spider import SpiderController

        self.controller = SpiderController()
        self.previous_spider = self.controller.get_previous_spider(self.index)
        
        super(SeleniumSpider, self).__init__(*args, **kwargs)
        
    def start_requests(self):
        return super().start_requests()
    
    def parse(self, response):
        # initialize handler
        pass
        
    def closed(self, reason):
        self.json_settings["index"] = self.index
        self.json_settings["request"] =  self.request
        self.json_settings["response"] = self.response
        
        self.controller.update_spider(self.json_settings, self.index)

        # start next spider process       
        if(self.index != len(self.controller.spiders) - 1):
            self.controller.start_spider_process(self.index +1)
        else:
            self.handler.stop_driver()
            print(reason)
            os.kill(os.getpid(), signal.SIGINT)