import scrapy
from scrapy.http import FormRequest, Response
from scraper.util.file_util import read_json_file, overwrite_json_file,append_json_file
from scrapy.crawler import CrawlerProcess

class BaseSpider(scrapy.Spider):
    name = "base"
 
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
        super(BaseSpider, self).__init__(*args, **kwargs)
        
    def parse(self, response):
        for xpath in self.xpaths:
            self.output_xpaths.append(response.xpath(xpath).getall())
            
        for selector in self.selectors:
            self.output_selectors.append(self.response.css(selector).getall())
    
        # test login token
        # self.form_data["loginToken"] = response.xpath('//input[contains(@name, "login")]/@value').getall()
   
        if len(self.form_data) > 0:
            return FormRequest.from_response(response, formdata=self.form_data, callback=self.form_data_response)

        for xpath in self.download_link_xpaths:
            self.download_links.extend(response.xpath(xpath).getall())
                        
        # download files
        for link in self.download_links: 
            yield scrapy.Request(link, callback=self.download_files)
        
        
    def form_data_response(self, response):
        links = response.xpath(
            '//a[contains(@href, "course/view.php")]/@href').getall()
      
    def download_files(self, response):
        file_name = response.url.split("/")[-1]
        
        with open(file_name, "wb") as f:
            f.write(response.body)
    
    def closed(self, reason):
        # update json settings
        self.json_settings["output_xpaths"] = self.output_xpaths
        self.json_settings["output_selectors"] = self.output_selectors
        self.json_settings["index"] = self.index
        append_json_file("json/spiders.json", self.json_settings)