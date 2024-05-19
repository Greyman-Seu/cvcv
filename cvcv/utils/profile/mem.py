# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

try:
    from pympler import asizeof # to slow
except ImportError:
    asizeof = None

__all__=[
    "format_size",
    "get_variable_size",
    "get_variable_size_h"]

def format_size(size_bytes):
    """
    将字节大小转换为字节、KB、MB、GB的字符串表示形式
    """
    power = 1024  # 每个单位的字节数
    units = ["B", "KB", "MB", "GB"]
    index = 0
    while size_bytes >= power and index < len(units) - 1:
        size_bytes /= power
        index += 1
    return f"{size_bytes:.2f} {units[index]}"

def get_variable_size(variable, enable_pympler=False):
    """
    返回变量占用的内存大小（以字节为单位）
    """
    if asizeof is not None and enable_pympler:
        return asizeof.asizeof(variable)
    return sys.getsizeof(variable)

def get_variable_size_h(variable):
    """
    返回变量占用的内存大小的人类友好表示形式（字节、KB、MB、GB）
    """
    return format_size(get_variable_size(variable))
