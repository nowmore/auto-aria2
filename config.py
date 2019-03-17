
import os
import json
import threading
from defaultConfig import defaultConf

class config(object):
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        try:
            with open('config.json', 'r', encoding='utf8') as f:
                self.__dict__.update(json.loads(f.readlines()))
        except:
            self.__dict__.update(json.loads(defaultConf))
        pass

    def update(self):
        with open('config.json', 'w', encoding='utf8') as file:
            file.writelines(json.dumps(self.__dict__))
            
    def __new__(cls, *args, **kwargs):
        if not hasattr(config, "_instance"):
            with config._instance_lock:
                if not hasattr(config, "_instance"):
                    config._instance = object.__new__(cls)
        return config._instance
    pass

        