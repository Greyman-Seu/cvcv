# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest


test_level = "train"  # train


@pytest.mark.skipif(test_level == "test", reason="train only")
@pytest.mark.parametrize(
    ["_string", "_int", "_tuple"],
    [
        pytest.param("string1", 1, (True, True)),
        pytest.param("string2", 2, (False, False)),
    ],
)
def test_mulset_params(_string, _int, _tuple):
    print("test_mulset_params: ", _string, _int, _tuple)


if __name__ == "__main__":
    # used for debug
    test_mulset_params("string", 1, (True,))
    """
    用例里面 print/logging 输出都打印， -s 参数
    用例遇见失败就停止执行， -x 参数
    用例执行详情展示，-v 参数
    """
    pytest.main(["-svx", __file__])
