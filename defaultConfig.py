
import os
import sys

defaultConf = """
{{
    "aria2":
    {{
        "root": "{home}\\aria2",
        "downloadPath": "{home}\\Downloads",
        "config": "{home}\\aria2\\aria2.conf",
        "session": "{home}\\aria2\\aria2.session",
        "process": "{home}\\aria2\\aria2c.exe",
        "manifest": "{home}\\aria2\\manifest.json"
    }},
    "url":
    {{
            "aira2Config": "https://raw.githubusercontent.com/nowmore/personal-backup/master/aria2.conf",
            "aria2Release": "https://github.com/aria2/aria2/releases/latest",
            "btTracekers": "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt"
    }},
    "manifest":
    {{
        "name": "com.fuck.run",
        "description": "allowed chrome extention to run aria2",
        "path": "{pwd}",
        "type": "stdio",
        "allowed_origins": 
        [
            "chrome-extension://djcghbekabhnjejbhkoehmbiniojjhih/"
        ]
    }}
}}
""".format(home=os.environ["USERPROFILE"],
pwd=sys.argv[0]).replace('\\', '\\\\')


logConf = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                'format': '[%(asctime)s %(filename)s:%(lineno)d (%(levelname)s)] => %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "default": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": 'runAria2.log',
                'mode': 'w+',
                "maxBytes": 1024*1024*5,  # 5 MB
                "backupCount": 20,
                "encoding": "utf8"
            },
        },
        "root": {
            'handlers': ['default'],
            'level': "INFO",
            'propagate': False
        }
    }