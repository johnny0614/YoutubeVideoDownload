#!/usr/bin/python
#
# YoutubeVideoDownload -- a small and simple program for downloading Youtube Video File
# Copyright (C) 2012  Yu Zhou
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



import urllib
import urllib2
import sys
import time
from os import path
from urlparse import parse_qs

__author__ = (
    'Yu \'Johnny\' Zhou'
    )
    

class VideoInfo(object):
    """
    VideoInfo Class hold all information retrieved from www.youtube.com/get_video_info?video_id=
    [VIDEO_ID]
    """
    def __init__(self, video_url):
        request_url = 'http://www.youtube.com/get_video_info?video_id='
        if 'http://www.youtube.com/watch?v' in parse_qs(video_url).keys():
            request_url += parse_qs(video_url)['http://www.youtube.com/watch?v'][0]
        elif 'v' in parse_qs(video_url).keys():
            request_url += parse_qs(video_url)['v'][0]
        else :
            sys.exit('Error : Invalid Youtube URL Passing')
        request = urllib2.Request(request_url)
        self.video_info = parse_qs(urllib2.urlopen(request).read())

def thumbnail_url(videoinfo):
    """
    extract thumbnail's url from VideoInfo object and return its url
    """
    if not isinstance(videoinfo, VideoInfo):
        sys.exit('Error : method (thumbnail_url) invalid argument passing')
    return urllib.unquote_plus(videoinfo.video_info['thumbnail_url'][0])

def title(videoinfo):
    """
    extract title from VideoInfo object
    """
    if not isinstance(videoinfo, VideoInfo):
        sys.exit('Error : method (title) invalid argument passing')
    title = videoinfo.video_info['title'][0].decode('utf-8')
    return title

def video_file_urls(videoinfo):
    """
    extract video file's url from VideoInfo object and return them
    """
    if not isinstance(videoinfo, VideoInfo):
        sys.exit('Error : method(video_file_urls) invalid argument passing')
    url_encoded_fmt_stream_map = videoinfo.video_info['url_encoded_fmt_stream_map'][0].split(',')
    entrys = [parse_qs(entry) for entry in url_encoded_fmt_stream_map]
    url_maps = [dict(url=entry['url'][0]+'&signature='+entry['sig'][0], type=entry['type']) for entry in entrys]
    return url_maps

    
def downloader(url, filename, prefix_message=''):
    """
    download file from url
    """
    if path.exists(filename):
        sys.exit('Error : file already exists')

    request=urllib2.Request(url)
    file=open(filename, 'wb')
    link=urllib2.urlopen(request)
    meta=link.info()
    filesize=int(meta.getheader('Content-Length'))
    size_message = 'downloading file size is %d byte\n' %(filesize)
    
    buff_size=16384
    downloaded_size=0

    sys.stdout.write(prefix_message+'\n'+size_message+'\n')
    sys.stdout.flush()
    
    while True:
        buffer = link.read(buff_size)
        if not buffer:
            break
        downloaded_size += len(buffer)
        file.write(buffer)
        display = '%s .............. %d / %d' %(filename, downloaded_size, filesize)
        sys.stdout.write("\r"+display)
        sys.stdout.flush()

    time.sleep(1)
    sys.stdout.write('\n')
    sys.stdout.flush()
    file.close()

def __getFileExtension(type):
    if type.lower() == 'video/webm':
        return 'webm'
    if type.lower() == 'video/mp4':
        return 'mp4'
    if type.lower() == 'video/3gpp':
        return '3gp'
    if type.lower() == 'video/x-flv':
        return 'flv'
    return None

def __getFileName(videoinfo, type):
    if not isinstance(videoinfo, VideoInfo):
        sys.exit('Error : method(__getFileName) invalid argument passing')
    filename = title(videoinfo)+'.'+type
    return filename
    


        
        
    
   
    
    
    
    







