from typing import List
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from util.file_util import read_json_file, append_json_file

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

class SpiderController():
    spiders = []
    json_file = ''
    
    def __init__(self, json_file=None):
        self.json_file = json_file
        self.spiders = self.get_spiders(self.json_file)
        
    def get_spiders(self, json_file=None):
        # read spiders.json file
        spiders = []
        settings = read_json_file("json/spiders.json") if json_file is None else read_json_file(json_file)

        for index,s in enumerate(settings):
            s['index'] = index
            spider = Spider(json_object=s)
            spiders.append(spider)
        return spiders
    
    def create_spider_process(self, spider:Spider):
        process = CrawlerProcess(spider.custom_settings)
        process.crawl(spider.name, **spider.settings)    
        return process
    
    def start_spider_process(self, spider_index):
        process = self.create_spider_process(self.spiders[spider_index])
        if spider_index == len(self.spiders) -1:
            process.start()
            
if __name__ == "__main__":
    controller = SpiderController()
    controller.start_spider_process(0)