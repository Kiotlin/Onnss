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
import requests
from utility import utils
from utility import config

class QQMusic:
    music_search_api = 'http://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp'
    token_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?'
    music_dl_url = 'http://ws.stream.qqmusic.qq.com/'

    def __init__(self):
        self.keywords_dict = {}
        self.song_list = {}
        self.playlist_list = {}
        self.album_list = {}
        self.count = 0

    def download(self, song_dict):
        token_params = {
            'format': 'json205361747',
            'platform': 'yqq',
            'cid': '205361747',
            'songmid': song_dict['songmid'],
            'filename': 'C400' + song_dict['songmid'] + '.mp3',
            'guid': '126548448'
        }

        token_get = requests.get(url=token_url, params=token_params)
        data = json.loads(token_get)
        vkey = data['data']['items'].get('vkey')
        mp3_params = {
            'fromtag': '0',
            'guid': '126548448',
            'vkey': vkey
        }
        mp3_url = music_dl_url + token_params['filename']
        mp3_stream = requests.get(url=mp3_url, params=mp3_params).content

        return
        
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
    search_list = qqmusic.search_music('稻香')
    print(search_list)
