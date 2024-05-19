# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json
from cvcv.utils.path.fs import dir_exists_or_mkdir

__all__ = []


##############################################################################
#  txt
##############################################################################


def readtxt(_file, return_all=False, **kargs):
    """DEMO"""
    if return_all:
        return open(_file, **kargs).readlines()
    else:
        """
        for line in readtxt(xxx):
            pass
        """
        return open(_file, **kargs)


##############################################################################
#  json
##############################################################################
# def json_m_load(path_json):
#     if os.path.isfile(path_json):
#         with open(path_json, "r") as jf:
#             return json.load(jf)
#     else:
#         print(f"json file is not found. {path_json}")
#         return None


# def json_o_load(json_path):
#     with open(json_path, "r", encoding="utf-8") as file:
#         json_ob = json.load(file)
# return json_ob


def json_save(path_json, list_dict):
    dir_exists_or_mkdir(path_json)
    if isinstance(list_dict, list):
        json_save_m(path_json, list_dict)
    elif isinstance(list_dict, dict):
        json_save_o(path_json, list_dict)


def json_save_m(path_json, list_dict):
    with open(path_json, "w+") as jf:
        for _dict in list_dict:
            jf.write(json.dumps(_dict) + "\n")


def json_save_o(path_json, _dict):
    with open(path_json, "w+", encoding="utf-8") as jf:
        json.dump(_dict, jf, ensure_ascii=False)


def json_load(path_json):
    _list_ret = []
    for _dict_string in open(path_json, "r"):
        _list_ret.append(json.loads(_dict_string))
    if len(_list_ret) == 1:
        return _list_ret[0]
    return _list_ret
