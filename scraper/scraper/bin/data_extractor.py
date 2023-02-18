from scrapy.http import Response
from pathvalidate import is_valid_filename
import wget
import requests
import validators
import lxml.etree
import m3u8
import os

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
    
def download_images(image_urls):
    for url in image_urls:
        print(url)


def extract_from_xpaths(xpaths, response) -> None:
    return flatten([response.xpath(xpath).getall() for xpath in xpaths])

def extract_from_selectors(selectors, response) -> None:
    return flatten([response.css(selector).getall() for selector in selectors])

def download_videos(video_urls):
    # extract video urls
    m3u8_content_types = ['application/mpegurl', 'application/x-mpegurl',
                            'audio/mpegurl', 'audio/x-mpegurl']
    
    video_content_types = ['video/mp4', 'video/x-flv', 
                    'video/3gpp', 'video/ogg', 'video/webm']
    
    for url in video_urls:
       r = requests.get(url, stream=True)
       content_type = r.headers.get('Content-Type', None)
       content_length = r.headers.get('content-length', None)
       
       if content_type:
           content_type = content_type.lower()
           print(content_type)
           print(content_length)
     
       # m3u8 response types
       if content_type in m3u8_content_types:
            playlist = get_m3u8_playlist(r,url)
            r = requests.get(playlist.uri)
            segments = m3u8.loads(r.text).data.get('segments')
            
            copy_cmd = 'copy /b '
            for idx,segment in enumerate(segments):
                # connect segments together 
                r = requests.get(segment['uri'])
                filename = str(idx) +'.ts' 
                save_file(r, filename, content_length, 1024)
                
                if idx == len(segments)-1:
                    copy_cmd+= filename
                    copy_cmd+= ' all.ts'
                else:
                    copy_cmd+= filename + '+'
            print(copy_cmd)
            ffmpeg_cmd = 'ffmpeg -i all.ts -bsf:a aac_adtstoasc -acodec copy -vcodec copy all.mp4'
            # os.system(copy_cmd)
        
       # regular video types         
       if content_type in video_content_types:
           save_file(r, "file.mp4", content_length)
        

def save_file(response, file_name, content_length=None, chunk_size=256):
    dl = 0
    content_length = int(content_length)
    with open(file_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if content_length: # content length exists
                dl += len(chunk)
                done = int(50 * dl / content_length)
                print(done, "/", content_length)
            f.write(chunk)

def get_m3u8_playlist(response:Response,resolution=None):
    playlists = []
    m3u8_object = m3u8.loads(response.text)
 
    playlists = m3u8_object.data.get("playlists", [])
    playlists = [M3U8Playlist(p) for p in playlists]
    for p in playlists:
        if resolution == p.stream_info.resolution:
            return p
    print(len(playlists))
    return playlists[0]
    
      
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
    