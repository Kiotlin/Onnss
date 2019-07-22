#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Kiotlin
# DATE: 2019/07/18 
# TIME: 17:56:20

# DESCRIPTION: Generate links & requirement from qq music

import os
import re
import json
from bs4 import BeautifulSoup as bs
from utility import utils
from utility import config
import requests

class QQMusic:
    music_search_api = 'http://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp'
    token_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?'
    music_dl_url = 'http://ws.stream.qqmusic.qq.com/'
    save_path = './download/'

    def __init__(self):
        self.keywords_dict = {}
        self.song_list = {}
        self.playlist_list = {}
        self.album_list = {}
        self.count = 0

    def downloader(self, song_dict):
        token_params = {
            'format': 'json205361747',
            'platform': 'yqq',
            'cid': '205361747',
            'songmid': song_dict['songmid'],
            'filename': 'C400' + song_dict['songmid'] + '.m4a',
            'guid': '126548448'
        }

        # 第一次请求获取vkey
        token_get = requests.get(url=self.token_url, params=token_params).text
        print(token_get)
        data = json.loads(token_get)
        vkey = ''
        for item in data['data']['items']:
            vkey = item.get('vkey')
        if vkey == '': # 有些歌曲不开放下载
            print("该歌曲不支持下载") 
            return
            
        # 第二次请求获取mp3源
        mp3_params = {
            'fromtag': '0',
            'guid': '126548448',
            'vkey': vkey
        }
        mp3_url = self.music_dl_url + token_params['filename']
        mp3_stream = requests.get(url=mp3_url, params=mp3_params).content
        mp3_file_name = self.save_path + song_dict['name'] + '.m4a'
        utils.write_file(mp3_file_name, 'wb', mp3_stream)
        

    def search_music(self, name) -> list:
        '''
        [
            {'name': '晴天', 'songmid': 0039MnYb0qxYhV, 'singers': '周杰伦/'}, 
            {'name': '稻香', 'songmid': 003aAYrm3GE0Ac, 'singers': '周杰伦/'},
        ]
        '''
        params = {
            'format': 'json',
            'p': 1,
            'n': 10000,
            'w': name
        }

        session = requests.session()
        session.headers.update(config.fake_headers)
        session.headers.update(
            {"referer": "http://m.y.qq.com", "User-Agent": config.ios_useragent}
        )
        r = session.get(self.music_search_api, params=params).text
        data = json.loads(r)

        search_result = []
        for item in data['data']['song']['list']:
            if name in item.get('songname'):
                singers = ''
                for singer in item['singer']:
                    singers += singer.get('name') + '/'
                search_result.append({
                    'name': item.get('songname'),
                    'songmid': item.get('songmid'),
                    'singers': singers
                })
        return search_result

if __name__ == '__main__':
    qqmusic = QQMusic()
    search_list = qqmusic.search_music('七里香')
    for item in search_list:
        qqmusic.downloader(item)
