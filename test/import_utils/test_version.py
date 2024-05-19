# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from cvcv.utils.import_utils.version import version,check_version

def test_version():
    print(
        "pytest version: ",version(pytest)
    )

def test_check_version():
    if not check_version(version(pytest),["5","7"]):
        print("pytest version should be >5, <7")
    else:
        print("version pass.")
        
if __name__ == '__main__':
    #test_version()
    #test_check_version()
    pytest.main(["-svx", __file__])