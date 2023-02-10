from scrapy.http import Response, Request

class RequestMapper():    
    def __init__(self) -> None:
        pass
    
    def get_json_request(self, request:Request):
        request = {
                   "url": request.url,
                   "cookies": request.cookies,
                   "meta": request.meta,
                   "headers": request.headers.to_unicode_dict(),
                   "method": request.method
                   }
        return request
    
    def get_form_data(self, form_data:dict, response:Response):
        for key,val in form_data.items():
            val:str
            if val.startswith("//"): # xpath
                form_data[key] = response.xpath(val).get()
                
        print("SENDING FORM DATA...", form_data)
        return form_data
    
    # given a scrapy Response object, convert to json response 
    def get_json_response(self, response:Response):

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