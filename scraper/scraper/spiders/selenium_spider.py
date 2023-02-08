from spiders.base_spider import BaseSpider
from scraper.bin.selenium import SeleniumDriver

class SeleniumSpider(BaseSpider):
    name = "selenium"
    driver_type = 0
    json_settings = []
    index = 0
    options = []
    driver = None
    events = []
    
    def __init__(self, *args, **kwargs):
        super(SeleniumSpider, self).__init__(*args, **kwargs)
        
    def start_requests(self):
        return super().start_requests()
    
    def parse(self, response):
        # initialize driver
        driver = SeleniumDriver(self.json_settings)
        driver.start_driver()
        driver.handle_events()