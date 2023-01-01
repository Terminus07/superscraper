from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.util.file_util import read_json_file

class Spider():
    name = ''
    settings = ''
    custom_settings = ''
    json_file = ''
    
    def __init__(self, name, json_file):
        self.name = name
        self.json_file = json_file
        self.settings = read_json_file(self.json_file)
        self.custom_settings = get_custom_settings(self.settings['custom_settings'])

# custom project settings from spider.json file
def get_custom_settings(custom):
    settings = get_project_settings()
    for key in dict(custom):
        settings[key] = custom[key]
    return settings

spiders = [Spider('base', "json/secret.json")]

spider:Spider
for index, spider in enumerate(spiders):
    process = CrawlerProcess(spider.custom_settings)
    spider.settings['index'] = index
    process.crawl(spider.name, **spider.settings)
process.start()