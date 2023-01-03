from typing import List
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from util.file_util import read_json_file, append_json_file

class Spider():
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
        self.name =  self.settings["name"]  if name is None else name

    def get_custom_settings(self):
        project_settings = get_project_settings()
        custom_settings  = self.settings['custom_settings']
        for key in dict(custom_settings):
            project_settings[key] = custom_settings[key]
        return project_settings

class SpiderController():
    spiders = []
    
    def __init__(self):
        self.spiders = self.get_spiders()
    
    def get_spiders(self):
        #read json file
        spiders = []
        settings = read_json_file("json/spiders.json")
        for s in settings:
            spider = Spider(json_object=s)
            spiders.append(spider)
        return spiders

    def create_spiders_json(self, spiders:List[Spider]):
        pass
    
    def get_current_spider(self):
        pass
    
    def create_spider_process(self, spider_index):
        spider:Spider
        process = CrawlerProcess(spider.custom_settings)
        process.crawl(spider.name, **spider.settings)
        process.start()

controller = SpiderController()
spiders = controller.get_spiders()

# check if spider.json is valid
# get spiders from spiders.json
# create spiders from spiders.json
# 