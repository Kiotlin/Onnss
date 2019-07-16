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

         
    def delete_html(self):
        pwd_path = os.path.abspath(self.save_path)
        for root, dir, files in os.walk(pwd_path):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root,file)
                    os.remove(file_path)

    
    def write_file(self, file_name, mode, content, encoding=None):
        with open(file_name, mode, encoding=encoding) as f:
            f.write(content)

    def read_file(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()

    def __analysis_node(self, html):
        soup = bs(html, 'lxml')

        song_list_names = soup.select('.f-ff2.f-brk')[0].get_text().strip().replace('\n', '')
        self.song_list_name = re.sub(r'[\/:*?"<>|]', '-', song_list_names) # RegExp 
        if not os.path.exists(f'{self.save_path}{self.song_list_name}'):
            os.mkdir(f'{self.save_path}{self.song_list_name}')
        
        ul_node = soup.find(name='ul', attrs={'class': 'f-hide'})
        li_node = soup.find_all(name='li')
        for a_node in li_node:
            href_content = a_node.find('a').get('href')
            song_name = a_node.find('a').get_text() 
            yield {
                'href_content': href_content,
                'song_name': song_name
            }

    def __downloader(self, song_dict):
        self.count += 1
        song_id = song_dict.get('href_content').split('=')[-1]
        song_name = song_dict.get('song_name').strip().replace(r'\n', '')
        
        mp3_url = self.music_download_url + song_id + '.mp3'
        mp3_stream = requests.get(url=mp3_url, headers=self.headers).content
        mp3_file_name = f'{self.save_path}{self.song_list_name}/{song_name}.mp3'
        self.write_file(mp3_file_name, 'wb', mp3_stream)

    def run(self):
        # content = self.__crawl_html()
        # self.__analysis_node(content)
        self.delete_html()


if __name__ == '__main__':
    url = input('input: \n')
    netease_music = NeteaseMusic(url=url)
    netease_music.run()


