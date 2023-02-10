import scrapy
import os, signal
from scrapy.http import FormRequest, Response, Request
from scraper.bin.spider import Spider, SpiderController
from scraper.bin.requests import get_form_data, get_json_request, get_request_parameters, get_json_response
from scraper.bin.data_extractor import DataExtractor
from util.dict_util import update_dict

class BaseSpider(scrapy.Spider):
    name = "base"
    
    # spider controller
    controller = ''
        
    # spider json objects
    previous_spider = None
    next_spider = None
    previous_response_urls = []
    previous_response = None
    json_settings = []
    
    # inputs
    index = 0
    xpaths = []
    selectors = []
    xpath_selectors = []
    form_data = {}
    download_links = []
    download_link_xpaths = []
    request_params = []
    
    # outputs
    output_xpaths = []
    output_selectors = []
    requests = []
    responses = []
    requests = []
    response = {}
    request = {}

    
    def __init__(self, *args, **kwargs):
        self.json_settings = kwargs
    
        # get spider controller
        self.controller = SpiderController()
        self.previous_spider:Spider

        # get previous and next spiders, if they exist
        self.previous_spider = self.controller.get_previous_spider(self.index)
        self.next_spider = self.controller.get_next_spider(self.index)
        
        super(BaseSpider, self).__init__(*args, **kwargs)    

    # override start_requests
    def start_requests(self):
        
        # if no start_urls are defined
        if len(self.start_urls) == 0 and self.index == 0:
            error = "No start urls defined."
            raise AttributeError(error)
        
        for url in self.start_urls:
            self.request = Request(url, dont_filter=True)
            yield self.request  
        
            
    def extract_data(self, response:Response):
        
        # append to request and response arrays
        self.response = get_json_response(response)        
        self.request = get_json_request(response.request)
        
        self.responses.append(self.response)
        self.requests.append(self.request)
        
        # define extractor
        extractor = DataExtractor(response)
        
        # extract text 
        self.output_xpaths = extractor.extract_from_xpaths(self.xpaths)       
        self.output_selectors = extractor.extract_from_selectors(self.selectors)
                    
        # download link xpaths
        self.download_links = extractor.extract_from_xpaths(self.download_link_xpaths)
        DataExtractor.download_from_links(self.download_links)
 
    def parse(self, response:Response):
        # cookies = response.headers.to_unicode_dict() 
        # print("COOKIES",cookies.get('set-cookie'))
        
        # set cookies
        self.extract_data(response)
 
        # generate form data
        if len(self.form_data) > 0:
            self.form_data = get_form_data(self.form_data, response)
            self.request = FormRequest.from_response(response, formdata=self.form_data, 
                                            callback=self.form_data_response)
            yield self.request
    
    def form_data_response(self, response:Response):
        self.extract_data(response)
        self.request = get_json_request(self.request)
        self.response = get_json_response(response)        

    def closed(self, reason):
        # update json setting
        update_dict(vars(self), self.json_settings)
        self.controller.update_spider(self.json_settings, self.index)

        # start next spider process       
        if(self.index != len(self.controller.spiders) - 1):
            self.controller.start_spider_process(self.index +1)
        else:
            print(reason)
            os.kill(os.getpid(), signal.SIGINT)