# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__all__ = []
import time
from cvcv.tools.profile.time import today, get_time_stamp, Timer

timer = Timer("TEST")
sleep_time = 0.5


@timer.timeit
def timeit_func():
    time.sleep(sleep_time)
    print(f"time.sleep({sleep_time})")


def test_time():
    
                
    # test set node
    print("="*20+"pool"+"="*20)
    time_p = Timer.pool(8)
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
    
    
    # test h_format
    # print(timer.h_format(999)) # 999ms
    # print(timer.h_format(1000)) # 1s
    # print(timer.h_format(1000*5)) # 5s
    # print(timer.h_format(1000*5+ 99.9)) # 5s 99ms
    
    # test @timer.timeit
    timeit_func()

    # test context
    with Timer():
        time.sleep(sleep_time)
        print("test context")

    # toc tic
    timer = Timer("TEST")
    timer.tic()
    time.sleep(sleep_time)
    print("test toc tic")
    timer.toc()
    
    # test per loop
    print("test context per loop")
    t =  Timer("context per loop" ,per_iters=2)
    for _ in range(10):
        t.tic()
        time.sleep(sleep_time/10)
        t.toc()
    
    # test context
    with Timer() as t:
        t.calls = 10 - 1
        for _ in range(10):
            time.sleep(sleep_time/10)

            
    


if __name__ == "__main__":
    test_time()
