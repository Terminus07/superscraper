from scrapy.loader import ItemLoader
from scraper.items import FileItem

class Loader(ItemLoader):
    default_item_class = FileItem