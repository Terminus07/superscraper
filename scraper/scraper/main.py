from typing import List
from scrapy.http import FormRequest, Response, Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from util.file_util import read_json_file, overwrite_json_file, append_json_file
import json
from ast import literal_eval

class Spider():
    index = 0
    name = ''
    settings = ''
    custom_settings = ''
    json_file = ''
    
    def __init__(self, name=None, json_file=None, json_object=None):
        self.json_file = json_file
        
        if json_file == None:
            self.settings = json_object
        else:
            self.settings = read_json_file(self.json_file)
        
        self.custom_settings = self.get_custom_settings()
        self.index = self.settings["index"]
        self.name =  self.settings["name"]  if name is None else name

    def get_custom_settings(self):
        project_settings = get_project_settings()
        custom_settings  = self.settings['custom_settings']
        for key in dict(custom_settings):
            project_settings[key] = custom_settings[key]
        return project_settings
    
    def __str__(self):
        print("INDEX: ", self.index)
        print("NAME:", self.name)
        print("SETTINGS:", self.settings)
        return ""
    
class SpiderController():
    spiders = []
    output_spiders = []
    json_file = ''
    
    def __init__(self, json_file=None):
        self.json_file = json_file
        self.spiders = self.get_spiders(self.json_file)
        self.output_spiders = self.get_spiders("json/output.json")

    def get_spiders(self, json_file=None):
        # read spiders.json file
        spiders = []
        settings = read_json_file("json/spiders.json") if json_file is None else read_json_file(json_file)
        
        for index,s in enumerate(settings):
            s['index'] = index
            spider = Spider(json_object=s)
            spiders.append(spider)
        return spiders
    
    def get_previous_spider(self, spider_index):
        if spider_index != 0:
            previous_spider = self.output_spiders[spider_index-1]
            return previous_spider
        
    def get_current_spider(self, index):
        return self.spiders[index]

    def update_spider(self, spider_settings, spider_index):
        spider = self.spiders[spider_index]
        spider: Spider
        spider.settings = spider_settings
        self.spiders[spider_index] = spider
        
        # create output.json
        try:
            append_json_file("json/output.json", spider.settings)
        except Exception as e:
            print(e)
            
    def print_spiders(self):
        for spider in self.spiders:
            spider:Spider
            print(spider)
            
    def get_spider_process(self, spider:Spider):
        process = CrawlerProcess(spider.custom_settings)
        process.crawl(spider.name, **spider.settings)    
        return process
    
    def start_spider_process(self, spider_index):
        process = self.get_spider_process(self.spiders[spider_index])
        process.start(stop_after_crawl=False)

class RequestMapper():
    def __init__(self) -> None:
        pass
    
    def get_json_request(self, request:Request):
        request = {
                   "url": request.url
                   }
        print("REQUEST",request)
        
        return request
    
    # given a scrapy Response object, convert to json response 
    def get_json_response(self, response:Response):
        
        response =  {
        "url": response.url,
        "status": response.status,
        "headers": response.headers.to_unicode_dict(),
        "protocol": response.protocol,
        "ip_address": str(response.ip_address),
        "flags": response.flags,
        "certificate": str(response.certificate)
        }
        return response
    
    def get_response(self, json):
        response = Response(url=json["url"], 
                        status=json["status"], 
                        headers=json["headers"],
                        protocol=json["protocol"]
                        )
        print(response.headers)
    
    def get_request_from_response(self, response:Response):
        req = Request(url=response.url)
        return req
        
if __name__ == "__main__":
    controller = SpiderController()
    controller.start_spider_process(0)