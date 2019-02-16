#!/bin/env python
# -*- coding:utf-8 -*-

import re
from config import Conf
from comm import get_tracker

content = ''
upd_flag = False


def load_conf():
    global content
    f = open(Conf.config, 'r', encoding='utf-8')
    content = f.read()
    f.close()


def save_conf():
    if upd_flag:
        with open(Conf.config, 'w', encoding='utf-8') as f:
            f.write(content)


def upd_conf(key, value):
    global content, upd_flag
    if re.search('\\s%s=%s\\s' % (key, value.replace('\\', '\\\\')), content):
        return
    content = re.sub('.*%s=.*' % key, '%s=%s' % (key, value.replace('\\', '\\\\')), content)
    upd_flag = True


# def upd_conf(**args):
#     """
#     dir, input-file are keyword, so can not use dict
#     :param args:
#     :return:
#     """
#     load_conf()
#     for k, v in args.items():
#         upd_conf(k, v)
#     save_conf()


def upd_tracker():
    upd_conf('bt-tracker', get_tracker())




