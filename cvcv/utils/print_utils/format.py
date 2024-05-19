# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pprint
from dataclasses import dataclass
from prettytable import *


__all__ = []


##############################################################################
#  msg format
##############################################################################
# from pprint, pprint.pformat
pformat = pprint.pformat


# table
def format_table(
    list_table,
    head_row: list = None,
    head_col: list = None,
    style=DEFAULT,
    sortby=None,
    reversesort=True,
    return_string=True,
):
    """
    list_table: [[],[],xx]
    style:  DEFAULT、MSWORD_FRIENDLY、PLAIN_COLUMNS、RANDOM
    sortby: sortby colname

    usage::
        case1:
            print(
                format_table(
                    list_table=[
                        ["xx", "xy"],
                        ["yx", "yy"],
                    ]
                )
            )
        output:
            +---------+---------+
            | Field 1 | Field 2 |
            +---------+---------+
            |    xx   |    xy   |
            |    yx   |    yy   |
            +---------+---------+
        case2:
            print(
                format_table(
                    list_table=[
                        ["xx", "xy"],
                        ["yx", "yy"],
                    ],
                    head_row=["x", "y"],
                )
            )
        output:
            +----+----+
            | x  | y  |
            +----+----+
            | xx | xy |
            | yx | yy |
            +----+----+
        case3:
            print(
                format_table(
                    list_table=[
                        ["xx", "xy"],
                        ["yx", "yy"],
                    ],
                    head_col=["x", "y"],
                )
            )
        output:
            +---------+---------+---------+
            | Field 1 | Field 2 | Field 3 |
            +---------+---------+---------+
            |    x    |    xx   |    xy   |
            |    y    |    yx   |    yy   |
            +---------+---------+---------+
        case4:
            print(
                format_table(
                    list_table=[
                        ["xx", "xy"],
                        ["yx", "yy"],
                    ],
                    head_row=["x", "y"],
                    head_col=["x", "y"],
                )
            )
        output:
            +---+----+----+
            |   | x  | y  |
            +---+----+----+
            | x | xx | xy |
            | y | yx | yy |
            +---+----+----+
    """
    if head_col is not None:
        assert len(list_table) == len(head_col)
    if head_row is not None:
        assert len(list_table[0]) == len(head_row)
        if head_col is not None:
            head_row = [""] + head_row

    tb = PrettyTable(head_row)
    for row_i, row_data in enumerate(list_table):
        if head_col is not None:
            row_data = [head_col[row_i]] + row_data
        tb.add_row(row_data)

    if style is not None:
        tb.set_style(style)

    if sortby is not None:
        tb.get_string(sortby=sortby, reversesort=reversesort)

    if return_string:
        return tb.get_string()
    return tb


def format_table_add_row(tb, row):
    tb.add_row(row)
    return tb


def format_table_add_col(tb, colname, coldata):
    tb.add_column(colname, coldata)
    return tb


def format_table_params(_dict, return_string=False):
    """
    _dict = {
        "bs": 16,
        "ep": 100,
        "opti": "adam",
    }
    print(format_table_params(_dict))
    """
    list_table = list(_dict.items())

    tb = format_table(
        list_table,
        head_row=["param_name", "val"],
        return_string=False,
    )
    tb.align["param_name"] = "r"
    tb.align["val"] = "l"
    tb.border = False
    if return_string:
        return tb.get_string()
    return tb


##############################################################################
#  color
##############################################################################
@dataclass
class LogColor(object):
    BLACK = 30
    RED = 31  # default
    GREEN = 32


def format_msg_color(msg, color="r"):
    # usage:: print(format_msg_color("test"))
    if color == "r":
        color = LogColor.RED
    elif color == "g":
        color = LogColor.GREEN
    else:
        color = LogColor.BLACK
    return "\033[%dm%s\033[0m" % (color, msg)
