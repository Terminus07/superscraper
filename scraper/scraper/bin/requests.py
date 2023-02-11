from scrapy.http import Response, Request
import validators
import lxml.etree

def get_json_request(request:Request):
    request = {
                "url": request.url,
                "cookies": request.headers.to_unicode_dict().get('cookie'),
                "meta": request.meta,
                "headers": request.headers.to_unicode_dict(),
                "method": request.method
                }
        
    return request

def get_form_data(form_data:dict, response:Response):
    for key,val in form_data.items():
        val:str
        form_data[key] = validate_xpath(val, response)

    print("SENDING FORM DATA...", form_data)
    return form_data

def get_requests(start_urls):
    requests = []
    # check if urls is dict
    for url in start_urls:
        if type(url) is dict:
            headers = url.get('headers', None)
            cookies = url.get('cookies', None)
            url = url.get('url', '')
            print(cookies)
            print(headers)
            print(url)
            request = Request(headers=headers, cookies=cookies, url=url, dont_filter=True)
        else:
            request = Request(url=url, dont_filter=True)
        requests.append(request)
    return requests

def validate_xpath(value, response:Response) -> None:
    try:
        print("VAL", value)
        lxml.etree.XPath(value)
        return response.xpath(value).get() if response.xpath(value).get() else value
    except Exception as e:
        print(e)
    return value

def extract_links(values, response:Response = None):
    for idx, value in enumerate(values):
        values[idx] = value if validators.url(value) else validate_xpath(value, response)
    return values

def get_json_response(response:Response):

    response =  {
    "url": response.url,
    "status": response.status,
    "headers": response.headers.to_unicode_dict(),
    "protocol": response.protocol,
    "ip_address": str(response.ip_address),
    "flags": response.flags,
    "certificate": str(response.certificate)
    }
    return response
 
   