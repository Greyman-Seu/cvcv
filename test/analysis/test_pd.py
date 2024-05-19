# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import cvcv.tools.analysis.pd_tools as pdt


def test_pandas_tools():
    data = [
        {"x": 1, "y": 2, "z": "a"},
        {"x": 11, "y": 22, "z": "aa"},
        {"x": 111, "y": 222, "z": "aaa"},
        {"x": 1111, "y": 2222, "z": "aaaa"},
    ]
    pd_data = pdt.pd_from_dict(data)
    # print(pd_data)
    """
          x     y     z
    0     1     2     a
    1    11    22    aa
    2   111   222   aaa
    3  1111  2222  aaaa
    """

    pd_data = pdt.pd_drop_data(pd_data, pd_data[pd_data["x"] == 1].index)
    # print(pd_data)
    """
          x     y     z
    1    11    22    aa
    2   111   222   aaa
    3  1111  2222  aaaa
    """

    pd_data = pdt.pd_drop_data(
        pd_data, ["y"], axis=1
    )  #  https://www.bilibili.com/read/cv17303442/
    # print(pd_data)
    """
          x     z
    1    11    aa
    2   111   aaa
    3  1111  aaaa
    """
    pd_data = pdt.pd_drop_data(pd_data, [1], axis=0)
    # print(pd_data)
    """
         x     z
    2   111   aaa
    3  1111  aaaa
    """
    # pd_data = pdt.pd_drop_data(pd_data, pd_data.filter(like="a", axis=1).index)
    # print(pd_data)
    """
    df.filter(regex='a$',axis=1)
    df.filter(like='on',axis=0)#选择行中包含on 作者Hot_bird https://www.bilibili.com/read/cv17303442/ 
    """

    data = [
        {"x": 1, "y": 2, "z": "a"},
        {"x": 11, "y": 22, "z": "aa"},
        {"x": 111, "y": 222, "z": "aaa"},
        {"x": 1111, "y": 2222, "z": "aaaa"},
    ]
    pd_data = pdt.pd_from_dict(data)
    pd_data = pdt.pd_func_map(pd_data, "x", lambda x: x + 1)
    # print(pd_data)
    """
        x     y     z
    0     2     2     a
    1    12    22    aa
    2   112   222   aaa
    3  1112  2222  aaaa
    """
    pd_data = pdt.pd_func_map(pd_data, "x", lambda x: x + 2, outputkey="x_plus_2")
    # print(pd_data)
    """
        x     y     z  x_plus_2
    0     2     2     a         4
    1    12    22    aa        14
    2   112   222   aaa       114
    3  1112  2222  aaaa      1114
    """

    def func_test1(x, thr=200):
        if x["x"] < thr:
            return 200
        return x["x"]

    def func_test2(x):
        return x["x"] + x["y"]

    pd_data = pdt.pd_func_apply(pd_data, func_test1, axis=1, outputkey="func_test1")
    """
        x     y     z  x_plus_2  func_test1
    0     2     2     a         4         200
    1    12    22    aa        14         200
    2   112   222   aaa       114         200
    3  1112  2222  aaaa      1114        1112
    """
    pd_data = pdt.pd_func_apply(pd_data, func_test2, axis=1, outputkey="func_test2")
    # print(pd_data)
    """
        x     y     z  x_plus_2  func_test1  func_test2
    0     2     2     a         4         200           4
    1    12    22    aa        14         200          34
    2   112   222   aaa       114         200         334
    3  1112  2222  aaaa      1114        1112        3334
    """


if __name__ == "__main__":
    test_pandas_tools()
