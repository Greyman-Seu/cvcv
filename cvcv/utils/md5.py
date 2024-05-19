# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__all__ = ["string_to_md5", "list_string_to_md5"]

import hashlib


def string_to_md5(string):
    md5_val = hashlib.md5(string.encode("utf8")).hexdigest()
    return md5_val


def list_string_to_md5(string_list):
    string_list = sorted(string_list)
    string_list_concat = "_".join(string_list)
    return string_to_md5(string_list_concat)
