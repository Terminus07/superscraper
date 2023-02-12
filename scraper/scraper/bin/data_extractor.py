from scrapy.http import FormRequest, Response, Request
from pathvalidate import is_valid_filename
import wget
import requests
import validators
import lxml.etree

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

    
def download_from_links(links):
    for link in links:
        f = link.split("/")[-1]
        file =  f if is_valid_filename(f) else None

        try:
            wget.download(link, out=file)
        except Exception as e:
            print(e)

def get_form_data(form_data:dict, response:Response):
    for key,val in form_data.items():
        val:str
        form_data[key] = validate_xpath(val, response)

    print("SENDING FORM DATA...", form_data)
    return form_data

           
def validate_xpath(value, response:Response) -> None:
    try:
        lxml.etree.XPath(value)
        return response.xpath(value).getall() if response.xpath(value).get() else value
    except Exception as e:
        print(e)
    return value

def extract_links(values, response:Response = None):
    for idx, value in enumerate(values):
        values[idx] = value if validators.url(value) else validate_xpath(value, response)
    return values