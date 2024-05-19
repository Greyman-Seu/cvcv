# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__all__ = ["tmpdir", "tmpfile"]

import tempfile

tmpdir = tempfile.mkdtemp
"""
cvcv usage:: 
    tmpdir(dir="/home/xxx/tmp/")
"""

tmpdir_autodel = tempfile.TemporaryDirectory
"""
cvcv usage:: 
    with tmpdir_autodel() as _dir:
        print(_dir)
"""

tmpfile = tempfile.TemporaryFile
tmpfilename = tempfile.NamedTemporaryFile
"""
cvcv usage:: 
    with tmpfile() as _file:
        print(_file)
"""
