from scrapy.http import Response, Request
from scraper.bin.spider import SpiderController, Spider

def get_json_request(request:Request):
    request = {
                "url": request.url,
                "cookies": request.headers.to_unicode_dict().get('cookie'),
                "meta": request.meta,
                "headers": request.headers.to_unicode_dict(),
                "method": request.method
                }
        
    return request

def get_requests(start_urls, meta:dict):
    requests = []
    
    for url in start_urls:
        if not isinstance(url, dict):
            url = {"url": url}
            
        headers = url.get('headers', None)
        cookies = url.get('cookies', None)
        url = url.get('url', '')
        
        request = Request(headers=headers, cookies=cookies, url=url, meta=meta, dont_filter=True) 
        requests.append(request)
    return requests



def get_json_response(response:Response):

    return {
    "url": response.url,
    "status": response.status,
    "headers": response.headers.to_unicode_dict(),
    "protocol": response.protocol,
    "ip_address": str(response.ip_address),
    "flags": response.flags,
    "certificate": str(response.certificate)
    }
    