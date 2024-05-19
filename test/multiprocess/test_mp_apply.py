# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from cvcv.utils.general_utils.temputils import tmpfilename
from cvcv.utils.multiprocess.mp_apply_async import MultiProcess, MultiProcessLog


def func_io(_string):
    print(_string)
    with tmpfilename(mode="w+") as f:
        f.write(_string)


def test_apply_asyn_wo_log():
    mp = MultiProcess(4)
    for i in range(16):
        mp.push_job(func_io, ["*" * (i + 1)])
    mp.start_stepbystep()
    mp.start_multi()


@MultiProcessLog.get_func_worker
def func_io_wrap(_string):
    print(_string)
    with tmpfilename(mode="w+") as f:
        f.write(_string)


def test_apply_asyn_w_log():
    func_io_worker = func_io_wrap
    mp = MultiProcessLog(4, 16)
    for i in range(16):
        mp.push_job(func_io_worker, ["*" * (i + 1)])
    mp.start_stepbystep()
    mp.start_multi()


if __name__ == "__main__":
    # test_apply_asyn_wo_log()
    # test_apply_asyn_w_log()
    # pytest.main(["-svx", __file__])
    pytest.main(["-x", __file__])
