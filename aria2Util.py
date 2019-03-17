import requests
from config import config
import os
import re 
import tempfile
import zipfile
import configparser
import urllib
import logging
import json

def req(url):
    return requests.get(url)
def reqRpc(method, params=None):
    host = 'http://localhost:6800/jsonrpc'
    req = {
            'jsonrpc':'2.0', 
            'id':'qwer',
            'method':method
    }
    if params:
        req['params'] = params
    return urllib.request.urlopen(host, json.dumps(req).encode('utf8')).read()


def releast():
    return req(config().url['aria2Release']).content.decode('utf8')

class util(object):
    def __init__(self, *args, **kwargs):
        c = config()
        self.aria2 = c.aria2
        self.url = c.url
        self.content = ''
    
        self.parser = configparser.ConfigParser()
        try:
            self.parser.read(self.aria2['config'])
        except:
            pass
        
    def updateAria2(self):
        self.content = releast()
        version = os.popen(self.aria2['process'] + ' -v').read().split('\n')[0].split(' ')[2]
        if version != re.search('Release aria2\s(.*?\d)\s', self.content).group(1):
            self.getLatestRelease()

    def getLatestRelease(self):
        pattern = '/aria2/aria2/releases/download/release-.*-win-64bit-build1.zip'
        latestRelease = 'https://github.com' + re.search(pattern, self.content if self.content else releast()).group()
        with tempfile.TemporaryFile() as t:
            t.write(req(latestRelease).content)
            t.flush()

            with zipfile.ZipFile(t) as z:
                for sub in z.infolist():
                    if sub.filename.__contains__('aria2c.exe'):
                        with open(self.aria2['process'], 'wb') as f:
                            f.write(z.read(sub))
                        break

    def getConfig(self):
        text = req(self.url['aira2Config']).text
        self.parser.read_string(text)
        self.updateConfig()

    def updateConfig(self):
        p = self.parser
        if not p.__contains__('aria2'):
            self.getConfig()

        a = p['aria2']
        if not a.__contains__('dir') or a['dir'] != self.aria2['downloadPath']:
            a['dir'] = self.aria2['downloadPath']
        if not a.__contains__('input-file') or a['input-file'] != self.aria2['session']:
            a['input-file'] = self.aria2['session']
        if not a.__contains__('save-session') or a['save-session'] != self.aria2['session']:
            a['save-session'] = self.aria2['session']
        a['bt-tracker'] = req(self.url['btTracekers']).content.decode('utf8').replace("\n", ';').replace(";;", ';')

        with open(self.aria2['config'], 'w', encoding='utf8') as file:
            p.write(file)


    @staticmethod
    def run():
        d = config().aria2
        cmd = '%s --conf-path=%s' %(d['process'], d['config'])
        logging.info('run aria2[%s]', cmd)
        os.popen(cmd)

    @staticmethod
    def addTask(param):
        logging.info('add url[%s]')
        logging.info(reqRpc('aria2.addUri', param))
