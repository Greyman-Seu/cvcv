# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import inspect
import importlib
from importlib import import_module

__all__=[
    "import_from_string",
    "import_from_path",
]

def import_from_string(_module_string):
    """
    从字符串中import模块
    
    用例:
        _module_string = "cvcv.version"
        mod = import_module(_module_string)

    """
    mod = import_module(_module_string)
    return mod


def import_from_path(_module_path):
    """
    从完整路径中import模块
    
    用例:
        _module_string = "xxx/cvcv/utils/import_utils/version.py"
        mod = import_from_path(_module_string)
    """
    if inspect.ismodule(_module_path):
        return _module_path

    module_dir, module_path = os.path.split(_module_path)
    module_name, module_ext = os.path.splitext(module_path)
    spec = importlib.util.spec_from_file_location(module_name, _module_path)
    modulevar = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulevar)
    return modulevar