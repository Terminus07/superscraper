from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
import hashlib

class CustomImagePipeline(ImagesPipeline):
    def process_item(self, item, spider):
        return super().process_item(item, spider)