from seleniumwire.request import Request, Response

def get_json_requests(requests):
    arr = []
    
    for r in requests:
        if isinstance(r, Request):
            arr.append(
                {
                    "id": r.id,
                    "method": r.method,
                    "headers": get_headers_json(r.headers),
                    "url": r.url,
                    "date": str(r.date)
                }
            )        
    return arr

def get_json_responses(responses):
   arr = []
   for r in responses:
     if isinstance(r,Response):
         arr.append({
             "status_code": r.status_code,
             "headers": get_headers_json(r.headers),
             "date": str(r.date)
         })
        
   return arr

def get_headers_json(headers):
    h = {}
    for k, v in headers.items():
        h[k] = v
    return h

