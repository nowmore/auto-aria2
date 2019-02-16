#!/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
import os
tracker_url = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt'
config_url = 'https://raw.githubusercontent.com/nowmore/personal-backup/master/aria2.conf'
release_url = 'https://github.com/aria2/aria2/releases/latest'
host = 'https://github.com'


def get_tracker():
    return requests.get(tracker_url).text.replace("\n", ';').replace(";;", ';')


def get_config(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(requests.get(config_url).text)


def get_release():
    save = os.getcwd() + '\\aria2.zip'
    content = requests.get(release_url).content
    pattern = '/aria2/aria2/releases/download/release-.*-win-64bit-build1.zip'
    url = host + re.search(pattern, content.decode('utf-8')).group()
    if url.__eq__(host):
        return None
    file = requests.get(url).content
    with open(save, 'wb') as f:
        f.write(file)
    return save



