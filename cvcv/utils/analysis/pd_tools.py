# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pandas as pd

__all__ = [
    "pd_from_dict",
    "pd_drop_data",
    "pd_func_map",
    "pd_func_apply",
]

##############################################################################
#
# Based on:
# --------------------------------------------------------
# TODO: 整理到example里面
# https://pandas.pydata.org/docs/getting_started/tutorials.html
# https://aistudio.baidu.com/projectdetail/1555263?ad-from=1541#练习5-合并
# https://blog.csdn.net/yiyele/article/details/80605909
# https://www.bilibili.com/read/cv17303442/
# --------------------------------------------------------


def pd_from_dict(data: list):
    """
    usage:
        data: [
                {xx:xx},
                {xx:xx},
        ]
    """
    assert isinstance(data, list), "data type must be list(dict)"
    pd_data = pd.DataFrame.from_dict(data)
    return pd_data


def pd_drop_data(pd_data, index, **kwargs):
    """
    usage:
        input: pd_data, pd_data[pd_data["label"] == -1].index
    """
    pd_data = pd_data.drop(index, **kwargs)
    return pd_data


def pd_func_map(pd_data, key, func, outputkey=None):
    """
    usage:
        pd_data[outputkey] = pd_data["key"].map(
            lambda x: np.array(x)
        )

        multi condition:
            idx = pd_data[key].map(func)
            idx = idx & pd_data[key2].map(func2)
            or
            pd_data[np.logical_and(idx1,idx2)]
    """
    if outputkey is None:
        outputkey = key
    pd_data[outputkey] = pd_data[key].map(func)
    return pd_data


def pd_func_apply(pd_data, func, outputkey=None, **kwargs):
    """
    usage:
        kwargs: used to apply func or func
             apply func: axis 0/1
             func - example:
                def func(x, thr):
                    x1 = x[key1]
                    x2 = x[key2]
                    return x1+x2
    """
    if outputkey is None:
        pd_data = pd_data.apply(func, **kwargs)
    else:
        pd_data[outputkey] = pd_data.apply(func, **kwargs)
    return pd_data
