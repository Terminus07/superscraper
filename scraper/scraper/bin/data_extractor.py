from scrapy.http import Response
from pathvalidate import is_valid_filename
import wget
import requests
import validators
import lxml.etree
import m3u8
import os
import mimetypes
import re

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
     

def download_media(media_urls, file_path=None):
    # extract video urls
    m3u8_content_types = ['application/mpegurl', 'application/x-mpegurl',
                            'audio/mpegurl', 'audio/x-mpegurl']
    
    segment_content_types = []
    
    video_content_types = ['video/mp4', 'video/x-flv', 
                    'video/3gpp', 'video/ogg', 'video/webm']
    
    image_content_types = ['image/apng', 'image/avif', 'image/gif', 
                           'image/jpeg', 'image/svg+xml', 'image/png',
                           'image/webp']
    base_extension = ''
    video_urls = []
    image_urls = []
    m3u8_urls = []
    segment_urls = []
    
    
    
    for i,url in enumerate(media_urls):
    
       # check if valid url
        try:
            r = requests.get(url, stream=True)
            content_type = r.headers.get('Content-Type', None)
            content_length = r.headers.get('content-length', None)
            content_disposition = r.headers.get('content-disposition', None)

            base_extension = ''
            extension = ''
            file_path = ''
            
            # convert content_type to lowercase
            if content_type:
                content_type = content_type.lower() 

            # create list of urls for each type
            if content_type in video_content_types:
                video_urls.append(url)
                base_extension = '.mp4'
            
            if content_type in image_content_types:
                image_urls.append(url)
                base_extension = '.jpeg'
            
            if content_type in segment_content_types:
                segment_urls.append(url)

            if content_type in m3u8_content_types:
                m3u8_urls.append(url)
                base_extension = '.m3u8'
   
            # check extension
            extension = mimetypes.guess_extension(content_type)
          
            if not extension:
                extension = base_extension

            # get file path name
            if not file_path:
                if content_disposition:
                    file_path = re.findall("filename=(.+)", content_disposition)[0]
                else:
                    file_path = str(i)
            file_path = file_path + extension
            
            save_file(r, file_path, content_length)
            print("INDEX",i, content_type, extension)
            
        except Exception as e:
                print(e)
    return image_urls, video_urls, m3u8_urls, segment_urls

def save_file(response, file_name, content_length=None, chunk_size=256):
    dl = 0
    content_length = int(content_length)
    with open(file_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if content_length: # content length exists
                dl += len(chunk) 
                print(dl, "/", content_length)
            f.write(chunk)

def get_m3u8_playlist(file_path,resolution=None):
    playlists = []
    m3u8_object = m3u8.loads(file_path)
 
    playlists = m3u8_object.data.get("playlists", [])
    playlists = [M3U8Playlist(p) for p in playlists]
    for p in playlists:
        if resolution == p.stream_info.resolution:
            return p
    return playlists[0]


def segments_download(segments, dest=None):
    pass

def m3u8_download(m3u8_file, dest):

    try:
        # convert ts/m3u8 to mp4
        ffmpeg_command = "ffmpeg -i {0} -acodec copy -bsf:a aac_adtstoasc -vcodec copy {1}".format(m3u8_file, dest)
        os.system(ffmpeg_command)
    except Exception as e:
        print(e)  
    # os.system(copy_cmd)  

def wget_download(links):
    for link in links:
        f = link.split("/")[-1]
        file =  f if is_valid_filename(f) else None

        try:
            wget.download(link, out=file)
        except Exception as e:
            print(e)

def get_form_data(form_data:dict, response):
    for key,val in form_data.items():
        val:str
        form_data[key] = validate_xpath(val, response)

    print("SENDING FORM DATA...", form_data)
    return form_data

           
def validate_xpath(value, response) -> None:
    try:
        lxml.etree.XPath(value)
        return response.xpath(value).getall() if response.xpath(value).get() else value
    except Exception as e:
        print(e)
        return value

def get_relative_link(base_url, link):
    if link[0:2] == '//':
        return link.replace('//','https://',1)
    
    relative_link = base_url + link
    return relative_link if validators.url(relative_link) else link

def extract_links(values, response = None, current_url = None):
    for idx, value in enumerate(values):
        if not validators.url(value):
            xpaths = validate_xpath(value, response)
            if xpaths != value:
                # if the xpath was not generated, extract relative links
                rel = []
                for xpath in xpaths:
                    rel.append(get_relative_link(current_url, xpath)) # if relative link was not generated, extract original value
                xpaths = rel

            value = xpaths
    
        values[idx] = value

    return flatten(values)

def extract_from_xpaths(xpaths, response) -> None:
    return flatten([response.xpath(xpath).getall() for xpath in xpaths])

def extract_from_selectors(selectors, response) -> None:
    return flatten([response.css(selector).getall() for selector in selectors])


def extract_items(item_fields:dict, response=None):
   
    items = []
    keys = []
    values = []
    length = 0 # max length of list of lists that will be extracted
    try:
        for k,v in item_fields.items():
            vals = validate_xpath(v, response)
            if len(vals) > length and isinstance(vals, list):
                length = len(vals)
            values.append(vals)
            keys.append(k)

        for i in range(0, length): # the true length of items
            d = {}
            for j ,key in enumerate(keys):
                value  = values[j][i] if len(values[j][i]) > 1 else ''
                d[key] = value
            items.append(d)
    except Exception as e:
        print(e)
    print(items)
    return items

def flatten(iterable):
    arr = []
    for i in iterable:
        if isinstance(i, list):
            arr.extend(i)
        else:
            arr.append(i)
    return arr
    