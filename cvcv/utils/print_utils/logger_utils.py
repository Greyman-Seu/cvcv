# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from loguru import logger

__all__ = ["get_logger", "get_logger_contextmanager", "Logger"]


def get_logger(path_logfile=None, disable_print=False, withtime_logfile=True):
    return Logger(path_logfile, disable_print, withtime_logfile)


def get_logger_contextmanager(
    path_logfile=None,
    disable_context=True,
    disable_context_level=logging.WARNING,
):
    """
    usage::

    with get_logger_contextmanager(
        path_logfile="data/test_log/log.log", disable_context_level=0
    ) as logger:
        logger.info("test")

    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    """

    return Logger(path_logfile, disable_context, disable_context_level)


##############################################################################
# Based on:
# --------------------------------------------------------
# https://zhuanlan.zhihu.com/p/549320692
# https://zhuanlan.zhihu.com/p/514838075
# --------------------------------------------------------
class Logger(object):
    """
    usage::

    _logger = get_logger(path_logfile="data/test_log/log.log")
    _logger.info("test")
    """

    def __init__(
        self,
        path_logfile=None,
        withtime_logfile=True,
        disable_print=False,
        disable_context=False,
        disable_context_level=logging.WARNING,
    ):
        self.disable_context = disable_context
        self.disable_context_level = disable_context_level
        self.logger = logger
        if path_logfile is not None:
            if withtime_logfile:
                path_logfile = path_logfile.replace(".log", "_{time}.log")
            self.logger.add(path_logfile, encoding="utf-8")

        if disable_print:
            logger.remove(handler_id=None)

    def __enter__(self):
        if self.disable_context:
            self.disable(self.disable_context_level)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.disable_context:
            self.disable(logger.logging.NOTSET)

    def disable(self, level):
        # level <= logging.level
        # level 0, print all
        # level 50, disable print
        """
        FATAL = CRITICAL
        ERROR = 40
        WARNING = 30
        WARN = WARNING
        INFO = 20
        DEBUG = 10
        NOTSET = 0
        """
        logging.disable(level)

    def debug(self, content):
        self.logger.debug(content)

    def warning(self, content):
        self.logger.warning(content)

    def info(self, content):
        self.logger.info(content)

    def error(self, content):
        self.logger.error(content)
