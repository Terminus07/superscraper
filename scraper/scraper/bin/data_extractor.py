from scrapy.http import FormRequest, Response, Request
from pathvalidate import is_valid_filename
import wget
import requests

class DataExtractor():
    response = None
    
    def __init__(self, response:Response) -> None:
        self.response = response
    
    def extract_from_xpaths(self, xpaths) -> None:
        return [self.response.xpath(xpath).getall() for xpath in xpaths]
        
    def extract_from_selectors(self, selectors) -> None:
        return [self.response.css(selector).getall() for selector in selectors]
    
    def download_videos(self):
        print("video")
    
    @staticmethod
    def download_from_links(links):
        for link in links:
            f = link.split("/")[-1]
            file =  f if is_valid_filename(f) else None

            try:
                wget.download(link, out=file)
            except Exception as e:
                print(e)
    