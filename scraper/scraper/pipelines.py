# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request

class ScraperPipeline:
    def process_item(self, item, spider):
        return item
    
class CustomPipeline(FilesPipeline):
   def file_path(self, request, response=None, info=None):
      meta = str(request.meta.get('file_name')[0])
      dir = str(request.meta.get('default_dir')[0])
      path = f'{dir}/{meta}'      
      return path
   
   def get_media_requests(self, item, info):
    urls = ItemAdapter(item).get(self.files_urls_field, [])
    meta = {'file_name': item['file_name'],
      'default_dir' : item['default_dir']
    }
    yield Request(url=urls[0], meta=meta)