# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import time
from cvcv.utils.multiprocess.mp_imap_unordered import imap_run


def _worker1(arg):
    time.sleep(0.2)
    print(arg)
    return True

def func(arg1, arg2):
    time.sleep(0.2)
    print(arg1,arg2)
    return True

def _worker2(params):
    # used for multi params input
    arg1, arg2 = params
    return func(arg1, arg2)

def test_imap_run1():
    task_list = [
        1,2,3
    ]
    imap_run(_worker1, task_list)
    return True
    
def test_imap_run2():
    task_list = [
        [1,2],
        [11,12],
        [21,22],
        [31,32],
    ]
    imap_run(_worker2, task_list)
    return True


if __name__ == '__main__':
    # test_imap_run1()
    # test_imap_run2() 
    pytest.main(["-svx", __file__])
