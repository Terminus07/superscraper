from scrapy.http import Response
from pathvalidate import is_valid_filename
import wget
import requests
import validators
import lxml.etree
import m3u8

class StreamInfo():
    bandwidth = None
    codecs = None
    audio = None
    resolution = None
    info = None
    def __init__(self, info) -> None:
        self.info = info
        if info:
            self.bandwidth = info.get("bandwidth")
            self.resolution = info.get("resolution")
    def __str__(self):
        return str(self.info)
    
class M3U8Playlist():
    stream_info:StreamInfo = None
    uri = None
    
    def __init__(self, playlist) -> None:
        self.stream_info = StreamInfo(playlist.get("stream_info", None))
        self.uri = playlist.get("uri", None)
    

def extract_from_xpaths(xpaths, response:Response) -> None:
    return [response.xpath(xpath).getall() for xpath in xpaths]

def extract_from_selectors(selectors, response:Response) -> None:
    return [response.css(selector).getall() for selector in selectors]

def download_videos(video_urls):
    # extract video urls
    for url in video_urls:
       r = requests.get(url, stream=True)
       content_type = r.headers.get('Content-Type', None).lower()
       m3u8_content_types = ['application/mpegurl', 'application/x-mpegurl',
                             'audio/mpegurl', 'audio/x-mpegurl']
       
       if content_type in m3u8_content_types:
            playlist = get_m3u8_playlist(r,url)
            r = requests.get(playlist.uri)
            segments = m3u8.loads(r.text).data.get('segments')
            print(segments)
       else:
           # regular video link (mp4)
           print(content_type)
           with open("file.mp4", "wb") as f:
            for chunk in r.iter_content(chunk_size=256):
                f.write(chunk)
     
def get_m3u8_playlist(response:Response,resolution=None):
    playlists = []
    m3u8_object = m3u8.loads(response.text)
    playlists = m3u8_object.data.get("playlists")
    playlists = [M3U8Playlist(p) for p in playlists]
    for p in playlists:
        if resolution == p.stream_info.resolution:
            return p
    
    return playlists[-1]
    
      
def wget_download(links):
    for link in links:
        f = link.split("/")[-1]
        file =  f if is_valid_filename(f) else None

        try:
            wget.download(link, out=file)
        except Exception as e:
            print(e)

def get_form_data(form_data:dict, response:Response):
    for key,val in form_data.items():
        val:str
        form_data[key] = validate_xpath(val, response)

    print("SENDING FORM DATA...", form_data)
    return form_data

           
def validate_xpath(value, response:Response) -> None:
    try:
        lxml.etree.XPath(value)
        return response.xpath(value).getall() if response.xpath(value).get() else value
    except Exception as e:
        print(e)
    return value

def extract_links(values, response:Response = None):
    for idx, value in enumerate(values):
        values[idx] = value if validators.url(value) else validate_xpath(value, response)
    
    return flatten(values)

def flatten(iterable):
    arr = []
    for i in iterable:
        if isinstance(i, list):
            arr.extend(i)
        else:
            arr.append(i)
    return arr
    