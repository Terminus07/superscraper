from scrapy.http import Response
from pathvalidate import is_valid_filename
import wget
import requests
import validators
import lxml.etree
import os
import mimetypes
import re
import sys
import m3u8
from urllib.parse import urlparse,urlsplit


def download_media(media_urls, file_path='', base_resolution=None):
    # extract video urls
    m3u8_content_types = ['application/mpegurl', 'application/x-mpegurl',
                            'audio/mpegurl', 'audio/x-mpegurl']
    
    segment_content_types = ['video/mp2t']
    
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
    file_name = None
    original_path = file_path
    
    for i,url in enumerate(media_urls):
    
       # check if valid url
        try:
            r = requests.get(url, stream=True)
      
            content_type = r.headers.get('Content-Type', None)
            content_length = r.headers.get('content-length', None)
            
            base_extension = ''
            extension = ''
            file_name = ''
            save = True
            
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
                base_extension = '.ts'

            if content_type in m3u8_content_types:
                m3u8_urls.append(url)
                base_extension = '.m3u8'
                save = False
                if base_resolution:
                   url, playlist = get_m3u8_playlist(r, base_resolution)
                   segments = get_m3u8_segments(playlist)
                   segments_download(segments)
                # m3u8_download(url, str(i))
   
            # check extension
            extension = mimetypes.guess_extension(content_type)
         
            if not extension:
                extension = base_extension

            file_name = str(i)
                
            t = file_name + extension
            file_path = os.path.join(original_path, t)
            file_path = '/'.join(file_path.split('\\'))

            if save:
                save_file(r, file_path, content_length)
               
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, exc_obj)
                
    return image_urls, video_urls, m3u8_urls, segment_urls

def save_file(response, file_name, content_length=None, chunk_size=256):
    dl = 0
    
    with open(file_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if content_length: # content length exists
                content_length = int(content_length)
                dl += len(chunk) 
                print(dl, "/", content_length)
            f.write(chunk)

def m3u8_download(url, index):
    try:
        # convert m3u8 to mp4
        ffmpeg_command = """ffmpeg -i "{0}" -c copy -bsf:a aac_adtstoasc {1}.mp4""".format(url, index)
        os.system(ffmpeg_command)
    except Exception as e:
        print(e) 

def segments_download(segments):
    file_names  = []
    print(segments)
 
    for idx,segment in enumerate(segments):
        # connect segments together 
        uri = segment.get('uri', None)
        r = requests.get(uri)
        filename = str(idx) +'.ts' 
        content_length = r.headers.get('content-length', None)
        save_file(r, filename, content_length, 2048)
        file_names.append(filename)

    copy_cmd = 'copy /b {0} all.ts && del {1}'.format("+".join(file_names)," ".join(file_names))
    ffmpeg_cmd = 'ffmpeg -i all.ts -bsf:a aac_adtstoasc -acodec copy -vcodec copy all.mp4'
    delete_cmd = 'del all.ts'
    os.system(copy_cmd)
    os.system(ffmpeg_cmd)
    os.system(delete_cmd)

def get_screen_resolution_difference(r1:str, r2:str):
    
    r1_width, r1_height = r1.split('x')
    r2_width, r2_height = r2.split('x')
    
    width = abs(int(r1_width) - int(r2_width))
    height = abs(int(r1_height) - int(r2_height))
    return (width, height)

def get_playlist_info(playlist):
    resolution = playlist.get("stream_info").get('resolution')
    uri = playlist.get("uri", None)
    return uri, resolution

def get_m3u8_playlist(response:Response, resolution):
    m3u8_object = m3u8.loads(response.text)
    playlists = m3u8_object.data.get("playlists", [])
    uri, res = get_playlist_info(playlists[0])
    index =0 
    res_diff = get_screen_resolution_difference(resolution, res)
    print(res, resolution)
    
    for i,p in enumerate(playlists):
        p_uri, p_resolution = get_playlist_info(p)
        
        if p_resolution == resolution:
            return p_uri
        
        diff = get_screen_resolution_difference(resolution, p_resolution)
        print("RES",resolution, p_resolution)
        
        if  diff < res_diff:
            uri = p_uri
            res = p_resolution
            index = i     
    return uri, playlists[index]

def get_m3u8_segments(playlist):
    r = requests.get(playlist.get('uri', None))
    segments = m3u8.loads(r.text).data.get('segments', None)
    return segments



    
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

def get_relative_link(base_url:str, link):
    if is_absolute(link):
        return link.replace('//','https://',1) if link[0:2] == '//' else link
    else:
        # get real base url
        split_url = urlsplit(base_url)
        base_url = "".join(base_url.split(split_url.path)[0]) if split_url.path else base_url
        relative_link = base_url + link
        return relative_link if validators.url(relative_link) else link

def is_absolute(url):
   return bool(urlparse(url).netloc)

def extract_links(values, response = None, current_url = None):
    for idx, value in enumerate(values):
        if not validators.url(value): # if it's not a valid url
            xpaths = validate_xpath(value, response)
            if isinstance(xpaths, list):
                for i,xpath in enumerate(xpaths):
                    xpaths[i] = get_relative_link(current_url, xpath)

            value = xpaths
    
        values[idx] = value
        
    return flatten(values)

def extract_from_xpaths(xpaths, response) -> None:
    return flatten([response.xpath(xpath).getall() for xpath in xpaths])

def extract_from_selectors(selectors, response) -> None:
    return flatten([response.css(selector).getall() for selector in selectors])


def extract_items(dictionary:dict, response=None):
    try:
        for k,v in dictionary.items():
            dictionary[k] = validate_xpath(v, response)
             
    except Exception as e:
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, exc_obj)
    
    return dictionary

def flatten(iterable):
    arr = []
    for i in iterable:
        if isinstance(i, list):
            arr.extend(i)
        else:
            arr.append(i)
    return arr
    