import threading
import queue
import requests
from bin.data_extractor import save_file, flatten
from util.file_util import read_json_file
import random

types = {
        0: 'proxies',
        1: 'proxies-basic',
        2: 'proxies-advanced'
    }

def fetch_proxies(type=0):
    # fetch proxies from websites or json file
    proxy_type = types.get(type)
    
    try:
        r = requests.get("https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/json/{0}.json".format(proxy_type))
        if r.status_code == 200:
            save_file(r, '{0}.json'.format(proxy_type))
    except Exception as e:
        print(e)

def get_proxies(type=1, rand=False, index=None, filters:dict={}):
    file = types.get(type)
    proxies = read_json_file('{0}.json'.format(file), "ignore")
   
    if isinstance(proxies, dict):
        ips = flatten(proxies.values())
    else:
        ips = [p.get('ip')+":"+str(p.get('port')) for p in proxies]
    
    if rand:
        index = random.randint(0,len(ips))
    
    return ips[index] if index else ips