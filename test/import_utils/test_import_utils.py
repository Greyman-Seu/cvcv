# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from cvcv.utils.path import root_dir
from cvcv.utils.import_utils.import_utils import (
    import_from_string,
    import_from_path
)

def test_import_from_string():
    _module_string = "cvcv.utils.import_utils.version"
    mod = import_from_string(_module_string)
    print("version package中存在以下方法:",dir(mod))

    _module_string = "cvcv.utils.import_utils.version.check_version"
    try:
        mod = import_from_string(_module_string)
    except:
        print("这东西不是个package, Sx")
    return True

def test_import_from_path():
    _module_path = os.path.join(
        root_dir,
        "cvcv/utils/import_utils/version.py"
    )
    mod = import_from_path(_module_path)
    return True

if __name__ == "__main__":
    test_import_from_string()
    test_import_from_path()