# coding:utf-8
import logging
import getpass
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class MyLog(object):
    def __init__(self):
        # 获取执行程序的用户
        self.user = getpass.getuser()
        # 1. 创建logger对象
        self.logger = logging.getLogger(self.user)
        # 设置logger的日志等级，下面定义的handler的日志等级一定要高于或等于这里的等级
        self.logger.setLevel(logging.DEBUG)

        self.logFile = sys.argv[0][0:-3] + '.log'
        # 2. 创建输出格式对象
        self.formatter = logging.Formatter('%(asctime)s %(name)-5s %(levelname)s: %(message)s')

        # 3. 创建文件handler，用于将日志写入文件
        self.logHand = logging.FileHandler(self.logFile, encoding='utf8')
        # 设置handler的输入格式
        self.logHand.setFormatter(self.formatter)
        # 设置handler的日志等级
        self.logHand.setLevel(logging.DEBUG)

        # 4. 创建输出到控制台的handler，用于将日志输入到控制台
        self.logHandSt = logging.StreamHandler()
        self.logHandSt.setFormatter(self.formatter)
        self.logHandSt.setLevel(logging.DEBUG)

        # 5. 添加handler
        self.logger.addHandler(self.logHand)
        self.logger.addHandler(self.logHandSt)

    # 日志的5个级别对应的写日志的方法
    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

if __name__ == '__main__':
    mylog = MyLog()
    mylog.debug("I'm debug 测试中文")
    mylog.info("I'm info")
    mylog.warn("I'm warn")
    mylog.error("I'm error 测试中文")
    mylog.critical("I'm critical")


