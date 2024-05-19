# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__all__ = []

from functools import partial
from contextlib import contextmanager


def test_func(_string, func_name="test_func"):
    print(func_name, " : ", _string)


@contextmanager
def demo_context(arg):
    """
    usage::
        with demo_context("test") as func:
            func("demo")

        with demo_context("test"):
            test_func("demo", "test_func")
    """
    print("__enter__")
    yield partial(test_func, func_name=arg)
    print("__exit__")


class DemoContext:
    """
    usage::
        with DemoContext("demo") as demo:
            demo.func()
    """

    def __init__(self, string="demo"):
        self._string = string

    def __enter__(self):
        print("__enter__")
        return self

    def __exit__(self, exc_type, exc_val, trackback):
        # must have exc_type, exc_val, trackbac
        print("__exit__")

    def func(self):
        print(self._string)
