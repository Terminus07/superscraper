import scrapy
import os, signal
from scrapy.http import FormRequest, Response
from scraper.bin.spider import Spider, SpiderController
from scraper.bin.scrapy_requests import get_requests, get_json_request,  get_json_response
from scraper.bin.data_extractor import *
from util.dict_util import update_dict

class BaseSpider(scrapy.Spider):
    name = "base"
    
    # spider controller
    controller = None
        
    # spider json objects
    previous_spider = None
    next_spider = None
    previous_response_urls = []
    previous_response = None
    json_settings = []
    
    # inputs
    index = 0
    xpaths = []
    start_urls = []
    selectors = []
    xpath_selectors = []
    form_data = {}
    download_links = []
    follow_links = []
    request_params = {}
         
    # outputs
    output_xpaths = []
    output_selectors = []
    requests = []
    responses = []
    response = {}
    request = {}
    
    def __init__(self, *args, **kwargs):
        self.json_settings = kwargs
        self.index = self.json_settings.get('index',0)
        
        # get spider controller
        self.controller = SpiderController()
        self.previous_spider:Spider
        self.next_spider:Spider
        
        # get previous and next spiders, if they exist
        self.previous_spider = self.controller.get_previous_spider(self.index)
        self.next_spider = self.controller.get_next_spider(self.index)
        
        super(BaseSpider, self).__init__(*args, **kwargs)    

    # override start_requests
    def start_requests(self):
        
        if self.previous_spider:
            self.start_urls.extend(self.previous_spider.follow_links)
        
        # if no start_urls are defined
        if len(self.start_urls) == 0:
            error = "No start urls defined."
            raise AttributeError(error)
            
        requests = get_requests(self.start_urls, self.request_params, self.controller, self.index)
        for request in requests:
            # if self.index == 1:
            #     print("cooki",request.cookies)
            self.request = request
            yield self.request
        
            
    def parse(self, response):
        self.extract_data(response)
        
        # generate form data
        if len(self.form_data) > 0:
            self.form_data = get_form_data(self.form_data, response)
            self.request = FormRequest.from_response(response, formdata=self.form_data, 
                                            callback=self.logged_in)

            return self.request
     
    def logged_in(self, response):
        self.extract_data(response)
        # print(response.xpath('//*[@id="action-menu-toggle-0"]/span/span[1]'))


    def extract_data(self, response:Response):  
        # append to request and response arrays
        self.response = get_json_response(response)        
        self.request = get_json_request(response.request)
        
        self.responses.append(self.response)
        self.requests.append(self.request)
        
        # extract text 
        self.output_xpaths = extract_from_xpaths(self.xpaths, response)       
        self.output_selectors = extract_from_selectors(self.selectors, response)
                    
        # generate download links
        self.download_links = extract_links(self.download_links, response)

        # extract follow links
        self.follow_links = extract_links(self.follow_links, response)
        
  
    def closed(self, reason):
        
        # update json settings
        update_dict(vars(self), self.json_settings)
        self.controller.update_spider(self.json_settings, self.index)
               
        # start next spider process    
        if(self.index != len(self.controller.spiders) - 1):
            self.controller.start_spider_process(self.index +1)
        else:
            print(reason)
            os.kill(os.getpid(), signal.SIGINT)