from scrapy.http import Response, Request
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
        try:
            lxml.etree.XPath(val)
            form_data[key] = response.xpath(val).get()
        except Exception as e:
            print(e)

    print("SENDING FORM DATA...", form_data)
    return form_data

def get_request_parameters(params:dict):
    # for each start url, a request is performed
    # if params is a dict, apply for all
    # if it's a list map request parameters for each
    
    
    print(params)

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
 
   