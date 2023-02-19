from scrapy.loader import ItemLoader
from scraper.items import ImageItem

class Loader(ItemLoader):
    default_item_class = ImageItem