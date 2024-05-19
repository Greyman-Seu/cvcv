# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

##############################################################################
#
# Based on:
# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__all__ = []

import time
import torch
import functools
from cvcv.tools.profile.time.time_utils import format_time

__all__ = ["Timer"]


class Timer:
    """
    A simple timer.

    Usage1::
        t =  Timer("context per loop" ,per_iters=2)
            for _ in range(10):
                t.tic()
                time.sleep(sleep_time/10)
                t.toc()
    Usage2::
        with Timer() as t:
            t.calls = 10 - 1
            for _ in range(10):
                func
                
    Usage3::
        with Timer():
            func
            
    Usage4::
        @Timer().timeit():
            def func
            
    Usage5: pool_discard
        time_p = Timer.pool_discard(8)
        not_print = 1
        for _ in range(10):
            step1 = time_p[1].set_node("step1 per 2", 2)
            with step1:
                time.sleep(0.01)
                
            step2 = time_p[2].set_node("step2 per3", 3, not_print=not_print)
            with step2:
                time.sleep(0.02)
                
            step3 = time_p[3].set_node("step3 per2", 2)
            with step3:
                time.sleep(0.03)
    
    """

    def __init__(self, name=None, iscuda=False, print_func=print, per_iters=1):
        self.name = name if name is not None else "default"
        self.per_iters = per_iters
        self.print_func = print_func
        self.cuda = iscuda  # torch.cuda.is_available()
        self.reset()
        
    def set_node(self, name=None, per_iters=1,not_print=False):
        if self.name == "default" and name is not None:
            self.name = name
        if per_iters != self.per_iters:
            self.per_iters = per_iters
        if not_print:
            self.print_func = None
        return self

    def reset(self):
        self.calls = 0
        self.total_time = 0
        self.tic_time = None

    def time(self):
        if self.cuda:
            torch.cuda.synchronize()
        return time.perf_counter()
    
    def cost(self, start_time):
        return self.time() - start_time
    
    def h_format(self, time_cost_ms):
        """
        ms,s,min
        """
        return format_time(time_cost_ms*1000)

    def tic(self):
        # using time.time instead of time.clock because time time.clock
        # does not normalize for multithreading
        self.tic_time = self.time()

    def toc(self):
        cost_time = self.time() - self.tic_time
        self.total_time += cost_time
        self.calls += 1
        if self.calls >= self.per_iters:
            self._log()
            self.reset()
        return cost_time
        
    def _log(self):
        if self.print_func is not None:
            self.print_func(
                "speed of {} is {} calls, cost time: {}, avg cost time {}".format(
                    self.name, self.calls, self.h_format(self.total_time), self.h_format(self.total_time / self.calls)
                )
            )

    def timeit(self, func):
        @functools.wraps(func)  # functools.wraps 旨在消除装饰器对原函数造成的影响
        def with_timer(*args, **kwargs):
            self.tic()
            ret = func(*args, **kwargs)
            self.toc()
            return ret
        return with_timer

    def __enter__(self):
        self.tic()
        return self

    def __exit__(self, exc_type, exc_val, trackback):
        self.toc()

    @classmethod
    def cuda(cls, name=None, iscuda=True, print_func=print, per_iters=1):
        return cls(name, iscuda, print_func, per_iters)
    
    @classmethod
    def pool(cls, timer_num=10):
        _pool = []
        for _ in range(timer_num):
            _pool.append(
                cls()
            )
        return _pool
