# -*- coding: utf-8 -*-

# @Function : 日志记录类
# @Time     : 2017/10/25
# @Author   : LiPb
# @File     : logger.py

import logging.handlers
import os
import sys


class Logger(logging.Logger):
    def __init__(self, filename=None):
        super(Logger, self).__init__(self)
        # 日志文件名
        if filename is None:
            filename = 'log.log'
        self.filename = filename

        # 用于写入日志文件 (每天生成1个，保留30天的日志)
        fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 30)
        fh.setLevel(logging.DEBUG)

        # 用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义输出格式
        formatter = logging.Formatter('[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] [%(process)s-%(thread)s]  %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.addHandler(fh)
        self.addHandler(ch)


log_path = os.path.dirname(sys.argv[0]) + '/log/'
if not os.path.exists(log_path):
    os.makedirs(log_path)
logging = Logger(log_path + '/log.log')
