from typing import List
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from util.file_util import read_json_file

class Spider():
    name = ''
    settings = ''
    custom_settings = ''
    json_file = ''
    
    def __init__(self, name, json_file):
        self.name = name
        self.json_file = json_file
        self.settings = read_json_file(self.json_file)
        self.custom_settings = self.get_custom_settings()

    def get_custom_settings(self):
        project_settings = get_project_settings()
        custom_settings  = self.settings['custom_settings']
        for key in dict(custom_settings):
            project_settings[key] = custom_settings[key]
        return project_settings

class SpiderController():

    def __init__(self):
        pass
    
    def get_spiders(self):
        #read json file
        spiders = read_json_file("json/spiders.json")
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

spiders = [Spider("base", "json/secret.json")]

controller = SpiderController()
print(controller.get_spiders())

# for index, spider in enumerate(spiders):
#     print(spider.custom_settings)
#     process = CrawlerProcess(spider.custom_settings)
#     spider.settings['index'] = index
#     process.crawl(spider.name, **spider.settings)
# process.start()