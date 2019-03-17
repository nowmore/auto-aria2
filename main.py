
"""
暂时只做启动功能
"""
from aria2Util import util
from env import env
import msg
import logging, logging.config
from defaultConfig import logConf
import sys

if __name__ == "__main__":
    logging.config.dictConfig(logConf)
    logging.info('process running')
    if (len(sys.argv) == 1 or sys.argv[1] == 'setup'):
        for a in sys.argv:
            logging.info(a)
        env.setup()
        sys.exit(0)

    env.setup()
    data = msg.recevice()
    msg.send('{"returnCoe":"0"}')
    logging.info(data)
    util.run()
    util.addTask(data.params)
    pass