from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from scrapy.http import Request

class CustomImagesPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        return super().process_item(item, spider)
    
    def file_path(self, request:Request, response=None, info=None, *, item=None):
        image_url_hash = hashlib.shake_256(request.url.encode()).hexdigest(5)
        image_perspective = request.url.split('/')[-2]
        image_filename = f'{image_perspective}'
        return image_filename