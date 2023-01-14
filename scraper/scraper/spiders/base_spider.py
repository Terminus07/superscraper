import scrapy
import os, signal
from scrapy.http import FormRequest, Response, Request
import wget
from pathvalidate import is_valid_filename
from scraper.main import RequestMapper

class BaseSpider(scrapy.Spider):
    name = "base"
    
    # spider controller and mapper
    controller = ''
    mapper = None
    
    # spider json objects
    previous_spider = None
    previous_response_urls = []
    previous_response = None
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
        
        # get previous spider, if it exists
        self.previous_spider = self.controller.get_previous_spider(self.index)
 
        super(BaseSpider, self).__init__(*args, **kwargs)    

    # override start_requests
    def start_requests(self):

        # check if previous spider exists to generate response links
        if self.previous_spider:
            self.previous_response_urls = self.previous_spider.settings["response_urls"]
            self.previous_response = self.previous_spider.response

        if len(self.start_urls) == 0 and self.index == 0:
            error = "No start urls defined."
            print(error)
            raise AttributeError(error)
        
        # regular urls
        for url in self.start_urls:
            self.request = Request(url, dont_filter=True)
            yield self.request
        
        # response urls (urls generated from previous spiders)
        for url in self.previous_response_urls:
            # get response object from json
            print(self.previous_response_urls)
            response = self.mapper.get_response(self.previous_response)
            self.request = self.mapper.get_request_from_json_response(url,response)
            yield self.request
            
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
            self.response_urls.extend(response.xpath(xpath).getall())

 
    def parse(self, response:Response):
               
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
            self.request = FormRequest.from_response(response, formdata=self.form_data, 
                                            callback=self.form_data_response)
            yield self.request
    
    def form_data_response(self, response:Response):
        # print(response.url)
        self.extract_data(response)
        self.request = self.mapper.get_json_request(self.request)
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