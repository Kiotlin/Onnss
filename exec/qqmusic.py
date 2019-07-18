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

class QQMusic:
    music_search_api = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?'

    def search_music(self, name) -> list:
        '''
        [
            {'name': '青花瓷', 'songmid': 5234112, 'singers': '周杰伦/'}, 
            {'name': '青花瓷 (2015江苏卫视新年演唱会)', 'songmid': 1337550384, 'singers': '周杰伦/'},
        ]
        '''
        params = {
            'aggr': 1,
            'cr': 1,
            'flag_qc': 0,
            'p': 1,
            'n': 10000,
            'w': name
        }
        return_json = requests.post(url=self.music_search_api, data=params).text
        data = json.loads(return_json)
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


