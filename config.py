#!/bin/env python
# -*- coding:utf-8 -*-

import os


class Conf:

    home = 'C:\\Users\\{}\\Documents\\aria2'.format(os.getenv('UserName'))
    config = home + '\\aria2.conf'
    download = home + '\\download'
    session = home + '\\session'
    tmp = home + '\\tmp'
    exe = 'aria2c.exe'
    process = home + '\\' + exe
    browser = 'C:\\Users\\n-\\Documents\\program\\Chrome\\Application\\chrome.exe'
    cmd = '%s --conf-path=%s' % (process, config)

