#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Kiotlin
# DATE: 2019/07/20 
# TIME: 23:57:30

# DESCRIPTION: utils.py


def write_file(file_name, mode, content, encoding=None):
    with open(file_name, mode, encoding=encoding) as f:
        f.write(content)

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()
