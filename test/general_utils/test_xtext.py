# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import os
from cvcv.utils.path import root_dir
from cvcv.utils.general_utils.xtext import json_save, json_load, readtxt


def test_readtxt():
    json_path = os.path.join(root_dir, "data/test_text", "multi_dict.json")
    print(readtxt(json_path, return_all=True))
    for txt in readtxt(json_path, return_all=False):
        print(txt.strip())


def test_json_save():
    one_dict = {"version": "0.0.1", "desc": "cvcv is all you need"}
    json_path = os.path.join(root_dir, "data/test_text", "one_dict.json")
    json_save(json_path, one_dict)
    json_path = os.path.join(root_dir, "data/test_text", "multi_dict.json")
    json_save(json_path, [one_dict for _ in range(5)])


def test_json_load():
    json_path = os.path.join(root_dir, "data/test_text", "one_dict.json")
    print(json_load(json_path))
    json_path = os.path.join(root_dir, "data/test_text", "multi_dict.json")
    print(json_load(json_path))


if __name__ == "__main__":
    # pytest.main(["-svx", __file__])
    pytest.main(["-x", __file__])
