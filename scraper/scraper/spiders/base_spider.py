import scrapy
import os, signal
from scrapy.http import FormRequest, Response, Request
import wget
from pathvalidate import is_valid_filename
from scraper.util.file_util import get_json_object
import json


class BaseSpider(scrapy.Spider):
    name = "base"
    
    # spider controller
    controller = ''
    previous_spider = None
    
    # spider json objects
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
        self.previous_spider:Spider
        self.previous_spider = self.controller.get_previous_spider(self.index)
        
        if self.previous_spider != None:
            print(self.previous_spider)
 
        super(BaseSpider, self).__init__(*args, **kwargs)    
    
    # override start_requests function from scrapy
    def start_requests(self):
        if len(self.start_urls) > 0:
            print("start")
            return super().start_requests()
        else:
            # get previous spider's response
            url  = "https://www.google.com"
            return [Request(url, dont_filter=True)]
    
    def parse(self, response):
        try:
            self.response = response.text
        except Exception as e:
            print(e)
            
        # extract text
        for xpath in self.xpaths:
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
        links = response.xpath(
            '//a[contains(@href, "course/view.php")]/@href').getall()

    def closed(self, reason):
        # update json settings
        self.json_settings["output_xpaths"] = self.output_xpaths
        self.json_settings["output_selectors"] = self.output_selectors
        self.json_settings["index"] = self.index
        # self.json_settings["request"] = self.request
        self.json_settings["response"] = self.response    
        
        # update spider
        self.controller.update_spider(self.json_settings, self.index)
     
        # start next spider process       
        if(self.index != len(self.controller.spiders) - 1):
            self.controller.start_spider_process(self.index +1)
        else:
            print("OK")
            os.kill(os.getpid(), signal.SIGINT)