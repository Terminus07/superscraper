import scrapy
import os, signal
from scrapy.http import FormRequest, Response, Request
import wget
from pathvalidate import is_valid_filename
from scraper.main import RequestMapper
import json

class BaseSpider(scrapy.Spider):
    name = "base"
    
    # spider controller and mapper
    controller = ''
    mapper = None
    
    # spider json objects
    previous_spider = None
    json_settings = []
    
    # inputs
    index = None
    xpaths = []
    selectors = []
    xpath_selectors = []
    form_data = {}
    download_links = []
    download_link_xpaths = []
    
    # outputs
    output_xpaths = []
    output_selectors = []
    request = {}
    response = {}
    
    # response
    previous_response_urls = []
    response_urls = []
    response_url_xpaths = []

    def __init__(self, *args, **kwargs):
        self.json_settings = kwargs
        self.index = kwargs['index']

        # get spider controller
        from scraper.main import SpiderController, Spider
        self.controller = SpiderController()
        self.mapper = RequestMapper()
        self.previous_spider:Spider
 
        if(self.index != 0):
            self.previous_spider = self.controller.get_previous_spider(self.index)
            self.previous_response_urls =  self.previous_spider.settings['response_urls']
        
        super(BaseSpider, self).__init__(*args, **kwargs)    

    # override start_requests
    def start_requests(self):
    
        if len(self.start_urls) == 0:
            error = "No start urls defined."
            print(error)
            raise AttributeError(error)
            
        # generate start_urls from xpaths
        print("START_URLS", self.start_urls)
        
        
        # regular urls
        for url in self.start_urls:
            self.request = Request(url, dont_filter=True)
            yield self.request

        
        # links
        # links that were previously found from response (response links)
        
        
            
    def extract_data(self, response:Response):
        # extract text
        for xpath in self.xpaths:
            self.output_xpaths.append(response.xpath(xpath).getall())
            
        for selector in self.selectors:
            self.output_selectors.append(response.css(selector).getall())
            
        # download link xpaths
        for d in self.download_link_xpaths:
            self.download_links.extend(response.xpath(d).getall()) 
            
        for xpath in self.response_url_xpaths:
            self.response_urls.append(response.xpath(xpath).getall())
 
    def parse(self, response):
        response:Response
        self.response = self.mapper.get_json_response(response)        
        self.request = self.mapper.get_json_request(self.request)

        self.extract_data(response)
                        
        for link in self.download_links:
            f = link.split("/")[-1]
            file =  f if is_valid_filename(f) else None

            try:
                wget.download(link, out=file)
            except Exception as e:
                print(e)
 
        # generate form data
        if len(self.form_data) > 0:
            self.form_data = self.mapper.get_form_data(self.form_data, response)
            yield FormRequest.from_response(response, formdata=self.form_data, 
                                            callback=self.form_data_response)
    
    def form_data_response(self, response):
        response:Response
        self.response = self.mapper.get_json_response(response)        


    def closed(self, reason):
        # update json settings
        self.json_settings["output_xpaths"] = self.output_xpaths
        self.json_settings["output_selectors"] = self.output_selectors
        self.json_settings["index"] = self.index
        self.json_settings["request"] =  self.request
        self.json_settings["response"] = self.response
        self.json_settings["response_urls"] = self.response_urls
        
        self.controller.update_spider(self.json_settings, self.index)

        # start next spider process       
        if(self.index != len(self.controller.spiders) - 1):
            self.controller.start_spider_process(self.index +1)
        else:
            print(reason)
            os.kill(os.getpid(), signal.SIGINT)