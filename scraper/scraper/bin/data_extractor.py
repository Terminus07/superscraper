from scrapy.http import FormRequest, Response, Request
from pathvalidate import is_valid_filename
import wget

class DataExtractor():
    response = None
    
    def __init__(self, response:Response) -> None:
        self.response = response
    
    def extract_from_xpaths(self, xpaths):
        outputs = []
        for xpath in xpaths:
            outputs.extend(self.response.xpath(xpath).getall())
        return outputs
    
    def extract_from_selectors(self, selectors):
        outputs = []
        for selector in selectors:
            outputs.extend(self.response.css(selector).getall())
        return outputs
    
    @staticmethod
    def download_from_links(links):
        for link in links:
            f = link.split("/")[-1]
            file =  f if is_valid_filename(f) else None

            try:
                wget.download(link, out=file)
            except Exception as e:
                print(e)
 