import pathlib
import os
import zipfile
import shutil
from config import Conf
from comm import get_config, get_release
from upd_config import upd_conf, upd_tracker, load_conf, save_conf


def get_process_count(process):
    return int(os.popen('tasklist /FI "IMAGENAME eq %s" | find /C "%s"' % (process, process)).read())


def kill(process):
    os.popen('taskkill /F /IM %s' % process)


def run_daemon(cmd):
    os.popen('start /b %s' % cmd)


def run_process(cmd):
    os.popen(cmd)


def exists(path):
    return pathlib.Path(path).exists()


def if_not_exists_create(path, mode):
    if not exists(path):
        if 0 == mode:
            os.mkdir(path)
        else:
            f = open(path, 'w')
            f.close()


def if_config_not_exists_download(path):
    if not exists(path):
        get_config(path)


def if_exe_not_exists_download(path):
    if not exists(path):
        file = get_release()
        z = zipfile.ZipFile(file)
        for sub in z.filelist:
            if sub.filename.__contains__('aria2c.exe'):
                z.extract(sub.filename)
                shutil.move(sub.filename, os.path.split(path)[0])
                os.rmdir(os.path.split(path)[0])
        os.rmdir(file)


def upd_configs():
    load_conf()
    upd_conf('dir', Conf.download)
    upd_conf('input-file', Conf.session)
    upd_conf('save-session', Conf.session)
    upd_tracker()
    save_conf()


def chk():
    if_not_exists_create(Conf.home, 0)
    if_not_exists_create(Conf.download, 0)
    if_not_exists_create(Conf.session, 1)
    if_config_not_exists_download(Conf.config)
    if_exe_not_exists_download(Conf.process)


def stop():
    if get_process_count(Conf.exe) > 0:
        kill(Conf.exe)


def run():
    if get_process_count(Conf.exe) == 0:
        run_daemon(Conf.cmd)
        run_process('%s http://aria2c.com/' % Conf.browser)


def init():
    chk()
    upd_configs()

