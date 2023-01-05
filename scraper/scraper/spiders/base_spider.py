import scrapy
import os, signal
from scrapy.http import FormRequest, Response, Request
import wget
from pathvalidate import is_valid_filename

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
    
    def start_requests(self):
        return super().start_requests()
    
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
    
    # get spider request and response
    
    
    def parse(self, response):
        # extract text
        response:Response
        
        # give response object to next spider
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