#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Kiotlin
# DATE: 2019/07/15 
# TIME: 15:58:35

# DESCRIPTION: Generate links & requirement from netease music

import os
import re
from bs4 import BeautifulSoup as bs
import requests

class NeteaseMusic:
    music_download_url = 'http://music.163.com/song/media/outer/url?id='
    playlist_url = 'https://music.163.com/playlist?id='

    def __init__(self, **kwargs):
        self.keywords_dict = {}
        for k, v in kwargs.items():
            self.keywords_dict[k] = v
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/69.0.3497.100 Safari/537.36',
            'referer': self.keywords_dict['url']
        }
        self.count = 0

    @property
    def generate_song_list_id(self):
        id = self.keywords_dict['url'].split('=')[-1]
        return id

    def __crawl_html(self):
        #....
        return
    
    def write_file(self, file_name, mode, content, encoding=None):
        with open(file_name, mode, encoding=encoding) as f:
            f.write(content)

    def read_file(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()


if __name__ == '__main__':
    url = input('input: \n')
    netease_music = NeteaseMusic(url=url)
    print(netease_music.generate_song_list_id)


