

import pathlib
import winreg
from config import config
import requests
from aria2Util import util
import os
import json
from defaultConfig import logConf
import logging

def exists(path):
    return pathlib.Path(path).exists()

class env(object):
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def setup():
        c = config()
        aria2Conf = c.aria2

        env.setupPath(aria2Conf['root'])
        env.setupPath(aria2Conf['downloadPath'])
        env.setupAria2Conf(aria2Conf['config'], c)
        env.setupFile(aria2Conf['session'], '')
        env.setupAria2c(aria2Conf['process'], c.url['aria2Release'])
        env.setupFile(aria2Conf['manifest'], json.dumps(c.manifest))
        env.setupReg(c.manifest['name'], aria2Conf['manifest'])

        if not exists('config.json'):
            c.update()
        pass

    @staticmethod
    def setupPath(path):
        if not exists(path):
            logging.info('path[%s] not exists, create...' % path)
            os.mkdir(path)

    @staticmethod
    def setupAria2Conf(path, url):
        if not exists(path):
            logging.info('aria2 config[%s] not exists, download...' % path)
            util().getConfig()
        pass

    @staticmethod
    def setupFile(path, content):
        if not exists(path):
            logging.info('file[%s] not exists, write...' % path)
            with open(path, 'w', encoding='utf8') as file:
                file.writelines(content)
        pass

    @staticmethod
    def setupAria2c(path, url):
        if not exists(path):
            logging.info('aria2 process[%s] not exists, get release...' % path)
            util().getLatestRelease()
            pass

    @staticmethod
    def setupReg(name,path):
        key = winreg.HKEY_CURRENT_USER
        subKey = 'Software\\Google\\Chrome\\NativeMessagingHosts\\%s' % name
        try:
            if(winreg.QueryValue(key, subKey) != path):
                logging.info('set reg key[HKEY_CURRENT_USER\\%s], value[%s]' % subKey, path)
                winreg.SetValue(key, subKey, winreg.REG_SZ, path)
        except:
            logging.info('set reg key[HKEY_CURRENT_USER\\%s], value[%s]' % subKey, path)
            winreg.SetValue(key, subKey, winreg.REG_SZ, path)
    pass