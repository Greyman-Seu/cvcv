# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import datetime

__all__ = ["today", "get_time_stamp"]

today = str(datetime.date.today())


def get_time_stamp(time_format="%Y%m%d%H%M%S"):
    time_stamp = time.strftime(
        # time_format, time.localtime(int(time.time()))
        time_format,
        time.localtime(),
    )
    return time_stamp

def format_time(milliseconds):
    seconds_ts = milliseconds/1000
    dt = datetime.datetime.fromtimestamp(seconds_ts)
    _min = dt.minute
    _s = dt.second
    _ms = dt.microsecond/1000
    _str = ""
    if _min:
        _str += f"{_min}min "
    if _s:
        _str += f"{_s}s "
    if _ms:
        _str += f"{_ms}ms"
    return _str