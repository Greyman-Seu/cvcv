# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import cvcv.tools.analysis.excel_tools as et
from cvcv.utils.general_utils.temputils import tmpdir, tmpdir_autodel


def test_excel_op():
    workbook, worksheet = et.create_xlsx("test_demo")
    et.add_cell(worksheet, row=1, col=1, val="test")

    et.set_row_h(worksheet, 1, 40)
    et.set_col_w(worksheet, 1, 50)

    # tmp_dir = tmpdir(dir="tmp/")
    # et.save(workbook, os.path.join(tmp_dir, "test_csv.xlsx"))
    with tmpdir_autodel() as tmp_dir:
        et.save(workbook, os.path.join(tmp_dir, "test_csv.xlsx"))


def test_create_xlsx_fromlist():
    list_data = [
        ["xx", "xy"],
        ["yx", "yy"],
    ]
    head_row = ["head1", "head2"]
    workbook, worksheet = et.create_xlsx_fromlist(list_data=list_data)
    with tmpdir_autodel() as tmp_dir:
        et.save(workbook, os.path.join(tmp_dir, "test_csv.xlsx"))

    workbook, worksheet = et.create_xlsx_fromlist(
        list_data=list_data, head_row=head_row
    )
    with tmpdir_autodel() as tmp_dir:
        et.save(workbook, os.path.join(tmp_dir, "test_csv.xlsx"))


if __name__ == "__main__":
    # test_excel_op()
    test_create_xlsx_fromlist()
