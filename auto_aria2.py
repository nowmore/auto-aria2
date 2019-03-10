
import os
import pathlib
import requests
import re
import zipfile
import shutil
import urllib, json
import base64
import time

class auto_aria2(object):

    def __init__(self, *args, **kwargs):
        self.home = 'C:\\Users\\{}\\aria2'.format(os.getenv('UserName'))
        self.config = self.home + '\\aria2.conf'
        self.download = 'C:\\Users\\{}\\Downloads'.format(os.getenv('UserName'))
        self.session = self.home + '\\session'
        self.exe = 'aria2c.exe'
        self.process = self.home + '\\' + self.exe
        self.cmd = '%s --conf-path=%s' % (self.process, self.config)
        self.curr_version = ''
        self.curr_version = self.version()
        self.chk()
        self.methods = {
            'save': 'aria2.saveSession',
            'shutdown':'aria2.forceShutdown',
            'pause': 'aria2.forcePauseAll',
            'start':'aria2.unpauseAll',
            'version':'ria2.getVersion',
            'addUri':'aria2.addUri',
            'addTorrent':'aria2.addTorrent'
        }
    
    def chk(self):
        if not self.exists(self.download):
            os.mkdir(self.download)

        if not self.exists(self.home):
            os.mkdir(self.home)
            with open(self.session, 'w') as f:
                f.close()
            self.init_config()
            self.get_aria2_release()
        elif not self.exists(self.config):
            self.init_config()
        elif not self.exists(self.session):
            with open(self.session, 'w') as f:
                f.close()
        elif not self.exists(self.process):
            self.get_aria2_release()

        pass


    def exists(self, path):
        return pathlib.Path(path).exists()

    def init_config(self):
        config_url = 'https://raw.githubusercontent.com/nowmore/personal-backup/master/aria2.conf'
        self.upd_config(requests.get(config_url).text)

    def get_aria2_release(self, version=None):
        release_url = 'https://github.com/aria2/aria2/releases/latest'
        pattern = '/aria2/aria2/releases/download/release-.*-win-64bit-build1.zip'
        host = 'https://github.com'

        temp = self.download + '\\aria2.zip'
        content = requests.get(release_url).content

        #如果最新版本跟当前版本一样，就不更新了
        if version and  re.search(pattern, content.decode('utf-8')).group().__eq__(version):
            print('$>: 最新版本： %s, 无须更新' % version)
            return

        if self.is_running():
            self.stop()

        url = host + re.search(pattern, content.decode('utf-8')).group()
        if url.__eq__(host):
            return 
        file = requests.get(url).content
        with open(temp, 'wb') as f:
            f.write(file)
            f.flush()
            f.close

        with zipfile.ZipFile(temp) as z:
            for sub in z.filelist:
                if sub.filename.__contains__(self.exe):
                    z.extract(sub.filename, path=self.home)
                    shutil.move(self.home+ '\\' + sub.filename, self.home)
                    shutil.rmtree(self.home + '\\' + os.path.split(sub.filename)[0])
                    break
        os.remove(temp)

    def get_bt_trackers(self):
        url = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt'
        return requests.get(url).text.replace("\n", ';').replace(";;", ';')

    def run(self):
        if not self.is_running():
            os.popen(self.cmd)
            time.sleep(5)
            self.start()

    def stop(self):
        if self.is_running():
            try:
                self.save()
                self.pause()
                self.shutdown()
                pass
            except :
                os.popen('taskkill /F /IM %s' % self.exe)
    

    def is_running(self):
        return (os.popen('tasklist /FI "IMAGENAME eq %s"' % self.exe).read().count(self.exe) > 0)


    def upd_config(self, contents):
        content = contents
        if content is None :
            with open(self.config, 'r', encoding='utf-8') as f:
                content = f.read()
            f.close()

        content = self.upd_by_key_value(content, 'dir', self.download)
        content = self.upd_by_key_value(content, 'input-file', self.session)
        content = self.upd_by_key_value(content, 'save-session', self.session)
        content = self.upd_by_key_value(content, 'bt-tracker', self.get_bt_trackers())

        with open(self.config, 'w', encoding='utf-8') as f:
            f.writelines(content)
            f.flush()
            f.close()

    def upd_by_key_value(self, content, key, value):
        if re.search('\\s%s=%s\\s' % (key, value.replace('\\', '\\\\')), content):
            return content
        return (re.sub('.*%s=.*' % key, '%s=%s' % (key, value.replace('\\', '\\\\')), content))

    def rpc_operate(self, method, params=None):
        host = 'http://localhost:6800/jsonrpc'
        req = {
            'jsonrpc':'2.0', 
            'id':'qwer',
            'method':method
        }
        if params:
            req['params'] = params
        return urllib.request.urlopen(host, json.dumps(req).encode('utf8')).read()

    def version(self):
        if self.curr_version:
            version = self.curr_version
        # 简单粗暴
        else:
            version = os.popen(self.process + ' -v').read().split('\n')[0].split(' ')[2]
        print('$>: 当前aria2版本为 ', version)
        return version
        # 通过rpc接口
        # method = 'aria2.getVersion'
        # return json.loads(self.rpc_operate(method),encoding='utf8')['result']['version']
    
    def update(self):
        self.get_aria2_release(self.version())

    def shutdown(self):
        self.rpc_operate(self.methods['shutdown'])

    def save(self):
        self.rpc_operate(self.methods['save'])

    def pause(self):
        self.rpc_operate(self.methods['pause'])

    def start(self):
        self.rpc_operate(self.methods['start'])

    def add_task(self, param):
        if param.__contains__('torrent'):
            self.rpc_operate(self.methods['addTorrent'], 
            [str(base64.b64encode(open(param, 'rb').read()), encoding='utf8')])
        else:
            self.rpc_operate(self.methods['addUri'],
            [[param]])

    def restart(self):
        self.stop()
        self.run()

    def update_configs(self):
        content = ''
        with open(self.config, 'r', encoding='utf8') as file:
            content = file.readlines()
            file.close()
        self.upd_config(content)
        self.restart()
    
    pass