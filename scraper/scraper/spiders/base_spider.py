import scrapy
import requests
import shutil
import os, signal
from scrapy.http import FormRequest, Response
from scraper.util.file_util import read_json_file, overwrite_json_file,append_json_file
from scrapy.crawler import CrawlerProcess
import wget
from pathvalidate import is_valid_filename
import time

class BaseSpider(scrapy.Spider):
    name = "base"
    
    #spider controller
    controller = ''
    
    # spider json objects
    json_settings = []
    json_spider = []
    
    # inputs
    index  = 0
    xpaths = []
    selectors = []
    xpath_selectors = []
    form_data = {}
    download_links = []
    download_link_xpaths = []
    
    # outputs
    output_xpaths = []
    output_selectors = []
    
    def __init__(self, *args, **kwargs):
        self.json_settings = kwargs
        
        # get spider controller
        from scraper.main import SpiderController
        self.controller = SpiderController()
        
        super(BaseSpider, self).__init__(*args, **kwargs)
        
    def parse(self, response):
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
        links = response.xpath(
            '//a[contains(@href, "course/view.php")]/@href').getall()

    def closed(self, reason):
        # update json settings
        self.json_settings["output_xpaths"] = self.output_xpaths
        self.json_settings["output_selectors"] = self.output_selectors
        self.json_settings["index"] = self.index
        
        print(self.index)
        print(self.output_xpaths)

        # update spider
        self.controller.update_spider(self.json_settings, self.index)
   
        # start next spider process       
        if(self.index != len(self.controller.spiders) - 1):
            self.controller.start_spider_process(self.index +1)
        else:
            os.kill(os.getpid(), signal.SIGINT)
