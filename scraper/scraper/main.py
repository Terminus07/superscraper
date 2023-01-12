from scrapy.http import FormRequest, Response, Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from util.file_util import read_json_file, append_json_file
import argparse
import os

class ArgParser():
    parser = None
    
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.subparser = self.parser.add_subparsers(dest="name")
        
        # spider command
        spider = self.subparser.add_parser('spider')
        spider.add_argument('type', choices=['base', 'selenium'], nargs='+')
        spider.add_argument('-d', '--directory', type=lambda s:self.check_file_extension(["json"],s) )
        
        # crawl command
        crawl = self.subparser.add_parser('crawl')
        crawl.add_argument('json', type=lambda s:self.check_file_extension(["json"],s), default="json/secret.json", nargs='?')

        # create args dictionary
        args = vars(self.parser.parse_args())

        if args['name'] is None:
            self.parser.error("No arguments passed.")
        else: 
            # start functions
            cmd = args['name']
            self.create_command(cmd, args)

    def create_command(self, command, args:dict):
        print(args, command)
        if command == "crawl":
            # check if passed spiders.json file exists
            file = args['json']
            controller = SpiderController(file)
            controller.start_spider_process(0)
            
        elif command == "spider":
            # generate spider.json file
            types= args['type']
            dir = args['directory']
            for type in types:
                # create json file of each type {base, selenium}
                data = read_json_file("json/"+type+".json")
                
                #  spiders.json is default directory for the file
                dir = "json/spiders.json" if dir is None else dir
                append_json_file(dir, data)
        
    def check_file_extension(self,choices,fname):
        ext = os.path.splitext(fname)[1][1:]
        if ext not in choices or ext == '':
            self.parser.error("Invalid file extension. File doesn't end with one of {}".format(choices))
        return fname
    
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
    
    def get_start_urls(self, response:Response):
        print()
    
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
    
    def get_response(self, json):
        response = Response(url=json["url"], 
                        status=json["status"], 
                        headers=json["headers"],
                        protocol=json["protocol"],
                        ip_address=json["ip_address"]
                        )
        print(response.headers)
        return response
    
    def get_request(self, json):
        request = Request(url=json['url'], 
                          headers=json['headers']
                          )
    
    def get_request_from_response(self, response:Response):
        req = Request(url=response.url)
        return req
    
class Spider():
    index = 0
    name = ''
    settings = ''
    custom_settings = ''
    json_file = ''
    
    def __init__(self, name=None, json_file=None, json_object=None):
        self.json_file = json_file
        self.settings  = json_object if json_file is None else read_json_file(self.json_file)
        self.custom_settings = self.get_custom_settings()
        self.index = self.settings["index"]
        self.name =  self.settings["name"]  if name is None else name

    def get_custom_settings(self):
        project_settings = get_project_settings()
        custom_settings  = self.settings['custom_settings']
        for key in dict(custom_settings):
            project_settings[key] = custom_settings[key]
        return project_settings
    
    def __str__(self):
        print("INDEX: ", self.index)
        print("NAME:", self.name)
        print("SETTINGS:", self.settings)
        return ""
   
class SpiderController():
    spiders = []
    output_spiders = []
    json_file = ''
    
    def __init__(self, json_file=None):
        self.json_file = json_file
        self.spiders = self.get_spiders(self.json_file)
        self.output_spiders = self.get_spiders("json/output.json")

    def get_spiders(self, json_file=None):
        # read spiders.json file
        spiders = []
        
        # change to spiders.json
        settings = read_json_file("json/secret.json") if json_file is None else read_json_file(json_file)
        
        for index,s in enumerate(settings):
            s['index'] = index
            spider = Spider(json_object=s)
            spiders.append(spider)
        return spiders
    
    def get_previous_spider(self, spider_index):
        if spider_index != 0:
            previous_spider = self.output_spiders[spider_index-1]
            return previous_spider

    def update_spider(self, spider_settings, spider_index):
        spider = self.spiders[spider_index]
        spider: Spider
        spider.settings = spider_settings
        self.spiders[spider_index] = spider
        
        # create output.json
        try:
            append_json_file("json/output.json", spider.settings)
        except Exception as e:
            print(e)
            
    def print_spiders(self):
        for spider in self.spiders:
            spider:Spider
            print(spider)
            
    def get_spider_process(self, spider:Spider):
        process = CrawlerProcess(spider.custom_settings)
        process.crawl(spider.name, **spider.settings)    
        return process
    
    def start_spider_process(self, spider_index):
        process = self.get_spider_process(self.spiders[spider_index])
        process.start(stop_after_crawl=False)
        
if __name__ == "__main__":
    parser = ArgParser()
    