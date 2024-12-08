# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

requires = []
with open("envs/pip/requirements.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line.startswith("#"):
            requires.append(line)

if __name__ == "__main__":
    # python setup.py bdist_wheel/install
    setup(
        # Metadata
        name="cvcv",
        version="0.0.2",
        author="copyer",
        description="cvcv: 'ctrl c'+'ctrl v' is all you need.",
        long_description=readme,
        # Package info
        packages=[x for x in find_packages(".") if x.startswith("cvcv")],
        zip_safe=False,
        include_package_data=True,
        install_requires=requires,
    )
