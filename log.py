#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
#
################################################################################

import sys
import os
import logging
import traceback

class MultiProcessFileLogHandler(logging.Handler):
    """
    多进程日志文件处理类
    """
    def __init__(self, file_path):
        self._fd = os.open(file_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
        logging.Handler.__init__(self)

    def emit(self, record):
        msg = "{}\n".format(self.format(record))
        os.write(self._fd, msg.encode('utf-8'))

class Log(object):
    """日志帮助类
    """
    logInstance = None
    formatter = logging.Formatter(
        '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    fileHandler = None
    streamHandler = None

    @staticmethod
    def initLogConf():
        """初始化log配置"""
        Log.streamHandler = logging.StreamHandler(sys.stdout)
        Log.streamHandler.setFormatter(Log.formatter)
        Log.streamHandler.setLevel(logging.INFO)

    @staticmethod
    def addFileHandle(file_path):
        """输出log到指定文件
        """
        Log.fileHandler = MultiProcessFileLogHandler(file_path)
        Log.fileHandler.setFormatter(Log.formatter)
        Log.getLogger().addHandler(Log.fileHandler)

    @staticmethod
    def getLogger():
        """获取Logger实例"""
        if Log.logInstance is None:
            Log.logInstance = logging.getLogger()
            Log.initLogConf()
            Log.logInstance.setLevel(logging.NOTSET)
            Log.logInstance.addHandler(Log.streamHandler)
        return Log.logInstance

    @staticmethod
    def closeStdout():
        """关闭stdout
        """
        Log.getLogger().removeHandler(Log.streamHandler)
        Log.streamHandler.flush()
        Log.streamHandler.close()
        Log.nullHandler = logging.NullHandler()
        Log.getLogger().addHandler(Log.nullHandler)

    @staticmethod
    def close():
        """关闭所有句柄
        """
        if Log.fileHandler is not None:
            Log.i('close file log handle')
            Log.getLogger().removeHandler(Log.fileHandler)
            Log.fileHandler.flush()
            Log.fileHandler.close()

    @staticmethod
    def d(msg):
        """Debug 日志"""
        Log.getLogger().debug(msg)

    @staticmethod
    def i(msg):
        """Info 日志"""
        Log.getLogger().info(msg)

    @staticmethod
    def i_box(msg):
        """Info 框框日志"""
        Log.getLogger().info('-' * 71)
        Log.i_box_inner(msg)
        Log.getLogger().info('-' * 71)

    @staticmethod
    def i_box_border():
        """Info 框框日志边框"""
        Log.getLogger().info('-' * 71)

    @staticmethod
    def i_box_inner(msg):
        """Info 框框日志内部"""
        lines = msg.split('\n')
        for line in lines:
            output = line[0:67]
            Log.getLogger().info('| %s%s |' % (output, ' ' * (67 - len(output))))
            length = len(line)
            for i in range(67, length, 65):
                output = line[i:i + 65]
                Log.getLogger().info('|   %s%s |' % (output, ' ' * (67 - len(output))))

    @staticmethod
    def w(msg):
        """Warning 日志"""
        Log.getLogger().warn(msg)
        Log.getLogger().warn(traceback.format_exc())

    @staticmethod
    def e(msg):
        """Error 日志"""
        Log.getLogger().error(msg)
        Log.getLogger().error(traceback.format_exc())

