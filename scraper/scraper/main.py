import argparse
import os
from bin.spider import SpiderController
from util.file_util import read_json_file, append_json_file
from util.constants import DIRECTORY, SPIDERS_DIRECTORY

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
                data_dir = DIRECTORY + "/" + type + ".json"
                data = read_json_file(data_dir)
                
                #  spiders.json is default directory for the file
                dir = SPIDERS_DIRECTORY if dir is None else dir
                append_json_file(dir, data)
        
    def check_file_extension(self,choices,fname):
        ext = os.path.splitext(fname)[1][1:]
        if ext not in choices or ext == '':
            self.parser.error("Invalid file extension. File doesn't end with one of {}".format(choices))
        return fname
  
if __name__ == "__main__":
    parser = ArgParser()
    