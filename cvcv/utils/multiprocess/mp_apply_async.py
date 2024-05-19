# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import math
import functools
import traceback
from tqdm import tqdm
from datetime import datetime
import multiprocessing
from multiprocessing import get_logger, Manager

__all__ = ["MultiProcess", "MultiProcessLog"]


class MultiProcess(object):
    def __init__(self, num_workers=16) -> None:
        num_workers = num_workers
        self.pool = multiprocessing.Pool(num_workers)
        self.task_list = []

    def push_job(self, func, params):
        self.task_list.append([func, params])

    def start_multi(self):
        self.pool_list = []
        for func, params in tqdm(self.task_list):
            self.pool_list.append(self.pool.apply_async(func, params))

        self.pool.close()
        self.pool.join()
        ret = [r.get() for r in self.pool_list]
        return ret

    def start_stepbystep(self):
        for func, params in tqdm(self.task_list):
            func(*params)


def error(msg, *args):
    return get_logger().error(msg, *args)


class LogExceptions(object):
    def __init__(self, callable):
        self.__callable = callable
        return

    def __call__(self, *args, **kwargs):
        try:
            result = self.__callable(*args, **kwargs)
        except Exception as e:
            error(traceback.format_exc())
            raise
        return result


class MultiProcessLog(object):
    """
    usage::

    @MultiProcessLog.get_func_worker
    def func_io_wrap(_string):
        print(_string)
        with tmpfilename(mode="w+") as f:
            f.write(_string)


    def test_apply_asyn_w_log():
        func_io_worker = func_io_wrap
        mp = MultiProcessLog(4, 16)
        for i in range(16):
            mp.push_job(func_io_worker, ["*" * (i + 1)])
        mp.start_stepbystep()
        or
        mp.start_multi()
    """

    def __init__(self, num_workers=16, total_task=-1) -> None:
        self.pool = multiprocessing.Pool(num_workers)
        self.task_list = []
        self.mp_bar = Manager().dict()
        self.mp_bar["start_time"] = datetime.now()
        self.mp_bar["total_task"] = total_task
        self.mp_bar["completed_task"] = 0
        self.mp_bar["num_proces"] = num_workers

    def push_job(self, func, params):
        self.task_list.append([func, params])

    def start_stepbystep(self):
        for func, params in tqdm(self.task_list):
            func(None, *params)

    def start_multi(self):
        self.pool_list = []
        for func, params in tqdm(self.task_list):
            self.pool_list.append(
                self.pool.apply_async(LogExceptions(func), [self.mp_bar, *params])
            )
        self.pool.close()
        self.pool.join()
        ret = []
        for r in self.pool_list:
            _ret = r.get()
            if _ret is not None:
                ret.append(_ret)
        return ret

    @staticmethod
    def get_func_worker(func):
        @functools.wraps(func)
        def func_worker(mp_bar, *arg, **kwarg):
            start_time_task = datetime.now()
            ret = func(*arg, **kwarg)

            if mp_bar is not None:
                mp_bar["completed_task"] += 1
                start_time = mp_bar["start_time"]
                total_task = int(mp_bar["total_task"])
                num_proces = int(mp_bar["num_proces"])
                len_num = len(str(total_task))
                completed_task = int(mp_bar["completed_task"])
                time_consumed = datetime.now() - start_time
                remainder_task = total_task - completed_task
                estimate_remiander_time = (
                    time_consumed
                    / completed_task
                    * math.ceil(remainder_task / num_proces)
                )
                estimate_compelted_time = datetime.now() + estimate_remiander_time

                single_task_consume = datetime.now() - start_time_task
                print(
                    f"{completed_task:>{len_num}}/{total_task}  开始时间：{str(start_time)[:-10]}  单任务耗时：{str(single_task_consume)[:-7]}  已运行:{str(time_consumed)[:-7]}  剩余：{str(estimate_remiander_time)[:-7]}  预计完成：{str(estimate_compelted_time)[:-7]}"
                )
            return ret

        return func_worker
