# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from distutils.version import LooseVersion

__all__=[
    "version",
    "check_version",
]

def version(module):
    return module.__version__

def check_version(_version, version_interval):
    """
    确认某个包
    """
    if isinstance(version_interval, str):
        raise ValueError("version_interval must be list")
    
    status = LooseVersion(_version) >= LooseVersion(
        version_interval[0]
    ) and LooseVersion(_version) <= LooseVersion(
        version_interval[1]
    )
    return status