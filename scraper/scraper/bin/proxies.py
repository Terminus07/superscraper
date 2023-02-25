import threading
import queue
import requests
from bin.data_extractor import save_file

types = {
        0: 'proxies-advanced',
        1: 'proxies-basic',
        2: 'proxies'
    }

def fetch_proxies(type=2):
    # fetch proxies from websites or json file
    proxy_type = types.get(type)
    
    try:
        r = requests.get("https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/json/{0}.json".format(proxy_type))
        if r.status_code == 200:
            save_file(r, '{0}.json'.format(proxy_type))
    except Exception as e:
        print(e)

def get_proxies(type=2):
    pass

def get_random_proxy():
    pass