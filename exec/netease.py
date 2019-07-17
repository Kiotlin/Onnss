#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Kiotlin
# DATE: 2019/07/15 
# TIME: 15:58:35

# DESCRIPTION: Generate links & requirement from netease music

import os
import re
import json
import uuid
from bs4 import BeautifulSoup as bs
import requests

class NeteaseMusic:
    music_download_url = 'http://music.163.com/song/media/outer/url?id='
    music_search_api = 'http://music.163.com/api/search/pc'
    save_path = './download/'
    dl_category = ''

    def __init__(self, **kwargs):
        self.keywords_dict = {}
        self.song_list = {}
        self.playlist_list = {}
        self.album_list = {}
        for k, v in kwargs.items():
            self.keywords_dict[k] = v

        category = self.keywords_dict['url'].split('com/')[-1].split('?')[0]
        if category == 'song':
            self.song_list = {
                'url': self.keywords_dict['url']
            }
            self.dl_category = category
        elif category == 'playlist':
            self.playlist_list = {
                'url': self.keywords_dict['url']
            }
            self.dl_category = category
        elif category == 'album':
            self.album_list = {
                'url': self.keywords_dict['url']
            }
            self.dl_category = category

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/69.0.3497.100 Safari/537.36',
            'referer': self.keywords_dict['url']
        }
        self.count = 0

    @property
    def __generate_song_id(self):
        return self.song_list['url'].split('=')[-1]
    
    @property
    def __generate_playlist_id(self):
        return self.playlist_list['url'].split('=')[-1]

    @property
    def __generate_album_id(self):
        return self.album_list['url'].split('=')[-1]

    def __crawl_html(self):
        if self.dl_category == 'song':
            file_path = f'{self.save_path}{self.__generate_song_id}.html'
        elif self.dl_category == 'playlist':
            file_path = f'{self.save_path}{self.__generate_playlist_id}.html'
        elif self.dl_category == 'album':
            file_path = f'{self.save_path}{self.__generate_album_id}.html'

        if os.path.exists(file_path):
            content = self.read_file(file_path)
            return content
        else: # if not exist, cache in local
            content = requests.get(url=self.keywords_dict.get('url'), headers=self.headers).text
            self.write_file(file_path, 'a', content, encoding='utf-8')
            return content

    def search_music(self, name) -> list:
        '''
        [
            {'name': '青花瓷', 'id': 5234112, 'artists': '何绮雯/缪晓铮/黄江琴/'}, 
            {'name': '青花瓷', 'id': 1337550384, 'artists': '葡萄bibo/'},
            {'name': '青花瓷', 'id': 281264, 'artists': '彭芳/'}, 
            {'name': '青花瓷', 'id': 454924421, 'artists': '张穆庭/'}, 
            {'name': '青花瓷', 'id': 521749035, 'artists': '张琼/'}
        ]
        '''
        params = {
            's': name,
            'offset': 0,
            'type': 1
        }
        return_json = requests.post(url=self.music_search_api, data=params).text
        data = json.loads(return_json)
        search_result = []
        for item in data['result']['songs']:
            if item.get('name') == name:
                artists = ''
                for arti in item['artists']:
                    artists += arti.get('name') + '/'
                search_result.append({
                    'name': item.get('name'),
                    'id': item.get('id'),
                    'artists': artists
                })
        return search_result

    @staticmethod    
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

        if self.dl_category == 'playlist':

            title = soup.select('.f-ff2.f-brk')[0].get_text().strip().replace(r'\n', '')
            self.title = re.sub(r'[\/:*?"<>|]', '-', title) # RegExp 
            if not os.path.exists(f'{self.save_path}{self.title}'):
                os.mkdir(f'{self.save_path}{self.title}')
            ul_node = soup.find(name='ul', attrs={'class': 'f-hide'})
            li_node = ul_node.find_all(name='li')
            for a_node in li_node:
                href_content = a_node.find('a').get('href')
                song_name = a_node.find('a').get_text() 
                yield {
                    'href_content': href_content,
                    'song_name': song_name
                }

        elif self.dl_category == 'song':

            title = soup.select('.f-ff2')[0].get_text().strip().replace(r'\n', '')
            self.title = re.sub(r'[\/:*?"<>|]', '-', title)
            if not os.path.exists(f'{self.save_path}{self.title}'):
                os.mkdir(f'{self.save_path}{self.title}')
            yield {
                'href_content': '/song?id=' + self.__generate_song_id,
                'song_name': self.title
            }

        elif self.dl_category == 'album':

            title = soup.select('.f-ff2')[0].get_text().strip().replace(r'\n', '')
            self.title = re.sub(r'[\/:*?"<>|]', '-', title)
            if not os.path.exists(f'{self.save_path}{self.title}'):
                os.mkdir(f'{self.save_path}{self.title}')
            ul_node = soup.find(name='ul', attrs={'class': 'f-hide'})
            li_node = ul_node.find_all(name='li')
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
        mp3_file_name = f'{self.save_path}{self.title}/{song_name}.mp3'
        self.write_file(mp3_file_name, 'wb', mp3_stream)

    def __404_detect(self, url):
        status_code = requests.get(url=url, headers=self.headers).status_code
        if status_code == '404':
            return True
        else:
            return False

    def run(self):
        try:
            html_content = self.__crawl_html()
            song_generator = self.__analysis_node(html_content)
            list(map(self.__downloader, song_generator))
        except Exception as e:
            import traceback
            traceback.print_exc()

def anti_spider_censor(url):
    url_header = url.split('/#')[0]
    url_footer = url.split('/#')[1]
    return url_header + url_footer 

if __name__ == '__main__':
    url = anti_spider_censor(input('input: \n'))
    netease_music = NeteaseMusic(url=url)
    netease_music.run()
    


