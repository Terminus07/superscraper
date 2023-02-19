from spiders.base_spider import BaseSpider
from scraper.bin.selenium import SeleniumDriver
from bin.selenium_requests import *
from scrapy.selector import Selector
from scraper.bin.data_extractor import *

class SeleniumSpider(BaseSpider):
    name = "selenium"
    json_settings = []
    index = 0
    driver = None
    body = None
    response = None
    save_requests = False
    
    def __init__(self, *args, **kwargs):
        self.json_settings = kwargs
        self.index = self.json_settings.get('index',0)
        super(SeleniumSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        self.driver = SeleniumDriver(self.json_settings)
        self.driver.start_driver()
        self.driver.load_urls()
        self.driver.handle_events()
        self.close(self, 'finished')

    def closed(self, reason):
       
        self.body = self.driver.get_html_response()
        self.response = Selector(text=self.body)  # get driver response in selector format
        
        # extract requests and responses
        if self.save_requests:
            self.requests = get_json_requests(self.driver.requests)
            self.responses = get_json_responses(self.driver.responses)
            
        self.extract_data(self.response)
        
        return super().closed(reason)
