"""
windows aria2自动下载，配置脚本
aria2路径：C:\\Users\\your_user_name\\aria2
aria2.exe, aria2.conf, session均在此目录
aria2的下载路径：C:\\Users\your_user_name\\Downloads
"""
# -*- coding:utf-8 -*-
try:
    from auto_aria2 import auto_aria2
except ModuleNotFoundError:
    print('requires not found! now we going to setup from you')
    import os
    os.popen('pip install requests')
    pass

import traceback
if __name__ == "__main__":

    obj = auto_aria2()
    obj.run()
    while True:
        cmd = input('$>: ')
        pos = cmd.find(' ')
        c = cmd if pos == -1 else cmd[:pos]

        try:
            if not obj.is_running():
                obj.run()
            if c in ['EXIT', 'QUIT', 'Q'] :
                print('$>: bye!')
                obj.stop()
                break
            elif c in ['P', 'PAUSE']:
                obj.pause()
            elif c in ['SAVE']:
                obj.save()
            elif c in ['START', 'CONTINUE']:
                obj.start()
            elif c in ['V', 'VERSION']:
                obj.version()
            elif c in ['U', 'UPDATE']:
                obj.update()
            elif c in ['A', 'ADD']:
                if pos == -1:
                    print('$>: 请输入要下载的url或者种子文件路径')
                    print('$>: A[DD] url/torrent')
                    continue
                obj.add_task(cmd[pos + 1:])
            else:
                print('''
$>: EXIT, QUIT, Q   停止aria2, 退出
    P, PAUSE        暂停下载
    SAVE            保存下载进度
    START           开始/继续下载
    V, VERSION      查看aria2版本
    U, UPDATE       检查更新
    A, ADD url      添加下载任务
    ''')
        except KeyboardInterrupt:
            obj.stop()
            break
        except Exception:
            traceback.print_exc()
            print('未知错误')
        


        
        