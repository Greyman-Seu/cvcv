# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import pytest
from cvcv.utils.multiprocess.asyncio_utils import asyncio_pool_run
from cvcv.utils.general_utils.temputils import tmpfilename


def func_io(_params):
    _string, _string2 = _params
    print(_string, _string2)
    with tmpfilename(mode="w+") as f:
        f.write(_string)


@pytest.mark.asyncio
async def test_asyncio_pool_run():
    params_list = []
    for i in range(16):
        params_list.append(["*" * (i + 1), "="])
    await asyncio_pool_run(func_io, params_list, max_workers=16)


if __name__ == "__main__":
    # 需要安装 pip install pytest-asyncio
    # asyncio.run(test_asyncio_pool_run())
    pytest.main(["-xsv", __file__])
