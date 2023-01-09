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
    current_spider = None
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

    def __init__(self, *args, **kwargs):
        self.json_settings = kwargs
        self.index = kwargs['index']

        # get spider controller
        from scraper.main import SpiderController, Spider
        self.controller = SpiderController()
        self.mapper = RequestMapper()
        self.previous_spider:Spider
        self.current_spider:Spider
        self.current_spider = self.controller.get_current_spider(self.index)
        
        if(self.index != 0):
            self.previous_spider = self.controller.get_previous_spider(self.index)
            print("PREVIOUS",self.previous_spider.settings)
        print("CURRENT",self.current_spider.settings)
        
        super(BaseSpider, self).__init__(*args, **kwargs)    
    
    # override start_requests function
    def start_requests(self):
        for url in self.start_urls:
            self.request = Request(url, dont_filter=True)
            yield self.request

    def parse(self, response):
        print("PARSE")
        response:Response
        self.response = self.mapper.get_json_response(response)        
        self.request = self.mapper.get_json_request(self.request)
        
        print("XPATHS", self.xpaths)
        # extract text
        for xpath in self.xpaths:
            print(xpath)
            self.output_xpaths.append(response.xpath(xpath).getall())
            
        for selector in self.selectors:
            self.output_selectors.append(self.response.css(selector).getall())

        # download files
        for d in self.download_link_xpaths:
            self.download_links.extend(response.xpath(d).getall())
                        
        for link in self.download_links: 
            # check if filename is valid
            f = link.split("/")[-1]
            file =  f if is_valid_filename(f) else None

            try:
                yield wget.download(link, out=file)
            except Exception as e:
                print(e)

        # test login token
        # self.form_data["loginToken"] = response.xpath('//input[contains(@name, "login")]/@value').getall()
   
        if len(self.form_data) > 0:
            return FormRequest.from_response(response, formdata=self.form_data, callback=self.form_data_response)
 
    def form_data_response(self, response):
        response:Response
        self.response = self.mapper.get_json_response(response)
        print("RESPONSE", self.response)

    def closed(self, reason):
        # update json settings
        print(self.output_xpaths)
        self.json_settings["output_xpaths"] = self.output_xpaths
        self.json_settings["output_selectors"] = self.output_selectors
        self.json_settings["index"] = self.index
        self.json_settings["request"] =  self.request
        self.json_settings["response"] = self.response
        self.controller.update_spider(self.json_settings, self.index)

        # start next spider process       
        if(self.index != len(self.controller.spiders) - 1):
            print("start")
            self.controller.start_spider_process(self.index +1)
        else:
            print("OK")
            os.kill(os.getpid(), signal.SIGINT)