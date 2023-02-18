import argparse
import os
from bin.spider import SpiderController
from util.file_util import *
from util.constants import DIRECTORY, SPIDERS_DIRECTORY, OUTPUT_DIRECTORY

class ArgParser():
    parser = None
    
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.subparser = self.parser.add_subparsers(dest="name")
        
        # spider command
        spider = self.subparser.add_parser('spider')
        choices = ['base', 'selenium']
        spider.add_argument('type', type=lambda s:self.check_spider_type(s, choices), default='base', nargs='+')
        spider.add_argument('-d', '--directory', type=lambda s:self.check_file_extension(["json"],s), default=SPIDERS_DIRECTORY )
        
        # crawl command
        crawl = self.subparser.add_parser('crawl')
        crawl.add_argument('json', type=lambda s:self.check_file_extension(["json"],s), default=SPIDERS_DIRECTORY, nargs='?')

        # create args dictionary
        args = vars(self.parser.parse_args())

        if args['name'] is None:
            self.parser.error("No arguments passed.")
        else: 
            # start functions
            cmd = args['name']
            self.create_command(cmd, args)

    def create_command(self, command, args:dict):
        commands_dict = {
            "crawl": self.crawl,
            "spider": self.spider
        }
        action = commands_dict.get(command)
        action(args)        
    
    @staticmethod
    def crawl(args:dict):
        # check if passed spiders.json file exists
        file = args.get('json', None)
        # reset output.json
        overwrite_json_file(OUTPUT_DIRECTORY, [])
        controller = SpiderController(file)
        controller.start_spider_process(0)
        
    @staticmethod
    def spider(args:dict):
        types = args['type'] 
        #  spiders.json is default directory for the file
        dir = args.get('directory', SPIDERS_DIRECTORY)
   
        overwrite_json_file(dir, [])
        for type in types:
            # check if type ends with .json
            ext = get_file_extension(type)
            data_dir = type if ext == 'json' else DIRECTORY + "/" + type + ".json"            
            data = read_json_file(data_dir)
            append_json_file(dir, data)
    
    def check_file_extension(self,choices,fname):
        ext = get_file_extension(fname)
        if ext not in choices or ext == '': 
            self.parser.error("Invalid file extension. File doesn't end with one of {}".format(choices))  
        return fname
    
    def check_spider_type(self, fname, choices):
        if fname in choices:
            return str(fname)
        else:
            fname = self.check_file_extension(["json"], fname)
        return fname
            
if __name__ == "__main__":
    parser = ArgParser()
    