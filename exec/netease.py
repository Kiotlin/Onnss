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
    save_path = './download/'

    def __init__(self, **kwargs):
        self.keywords_dict = {}
        for k, v in kwargs.items():
            self.keywords_dict[k] = v
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/69.0.3497.100 Safari/537.36',
            'referer': self.keywords_dict['url']
        }
        self.count = 0

    @property
    def __generate_song_list_id(self):
        return self.keywords_dict['url'].split('=')[-1]

    def __crawl_html(self):
        file_path = f'{self.save_path}{self.__generate_song_list_id}.html'
        if os.path.exists(file_path):
            content = self.read_file(file_path)
            print('read success!\n')
            return content
        else: # if not exist, cache in local
            content = requests.get(url=self.keywords_dict.get('url'), headers=self.headers).text
            self.write_file(file_path, 'a', content, encoding='utf-8')
            print('write success!\n')
            return content
            
        
    
    def write_file(self, file_name, mode, content, encoding=None):
        with open(file_name, mode, encoding=encoding) as f:
            f.write(content)

    def read_file(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()

    def __analysis_node(self, html):
        soup = bs(html, 'lxml')
        
        

    def run(self):
        content = self.__crawl_html()
        self.__analysis_node(content)


if __name__ == '__main__':
    url = input('input: \n')
    netease_music = NeteaseMusic(url=url)
    netease_music.run()


