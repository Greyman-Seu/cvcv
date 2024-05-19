# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from tqdm import tqdm
import multiprocessing as mp
from multiprocessing import Pool, set_start_method


__all__ = ["imap_run"]


def imap_run(worker, task_list, enable_spawn=False, processes=4):
    """
    def _worker(params):
        # used for func with multi params input
        arg1, arg2 = params
        return func(arg1, arg2)
    """
    if enable_spawn:
        if mp.get_start_method() != "spawn":
            set_start_method("spawn")

    with Pool(processes=processes) as p, tqdm(total=len(task_list)) as bpbar:
        for _ in p.imap_unordered(worker, task_list):
            bpbar.update()
