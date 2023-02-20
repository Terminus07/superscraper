import scrapy
import os, signal
from scrapy.http import FormRequest, Response
from scraper.bin.spider import Spider, SpiderController
from scraper.bin.scrapy_requests import *
from scraper.bin.data_extractor import *
from scrapy.selector import Selector
from util.dict_util import update_dict
from scraper.items import ImageItem

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
    save_requests = False
    index = 0
    xpaths = []
    start_urls = []
    selectors = []
    form_data = {}
    wget_links = []
    image_links = []
    media_links = []
    follow_links = []
    request_params = {}
    item_fields = {}
         
    # outputs
    extracted_xpaths = []
    extracted_selectors = []
    extracted_items = []
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
            self.request = request
            yield self.request
        
            
    def parse(self, response):
        self.extract_requests(response)
        self.extract_data(response)
        
        # generate form data
        if len(self.form_data) > 0:
            self.form_data = get_form_data(self.form_data, response)
            self.request = FormRequest.from_response(response, formdata=self.form_data, 
                                            callback=self.logged_in)

            return self.request
        
        # generate image links
        return {
                'image_urls': self.image_links
        }
           
     
    def logged_in(self, response):
        print("Logged in")
        self.extract_requests(response)
        self.extract_data(response)
      
    def extract_requests(self, response:Response):
         # append to request and response arrays
        if self.save_requests:
            self.response = get_json_response(response)        
            self.request = get_json_request(response.request)
            
            self.responses.append(self.response)
            self.requests.append(self.request)
    
    def extract_data(self, response):  
        # extract text 
        self.extracted_xpaths = extract_from_xpaths(self.xpaths, response)       
        self.extracted_selectors = extract_from_selectors(self.selectors, response)
        self.extracted_items = extract_items(self.item_fields, response)
  
        # extract links
        self.wget_links = extract_links(self.wget_links, response)
        self.follow_links = extract_links(self.follow_links, response)
        self.media_links  = extract_links(self.media_links, response) 
        self.image_links = extract_links(self.image_links, response)    
           
        # get relative links 
        self.media_links = get_relative_links(self.media_links, response)

        # downloaders
        download_media(self.media_links)
        wget_download(self.wget_links)
       
        
    def closed(self, reason):
        
        # update json settings
        update_dict(vars(self), self.json_settings)
        self.controller.update_spider(self.json_settings, self.index)
          
        # start next spider process    
        if(self.index != len(self.controller.spiders) - 1):
            self.controller.start_spider_process(self.index +1)
        else:
            print(reason)
            # open output.json
            # os.system("start code json_templates/secret/output.json")
            os.kill(os.getpid(), signal.SIGINT)