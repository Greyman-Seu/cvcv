# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import asyncio
from concurrent.futures import ProcessPoolExecutor


##############################################################################
#
# Based on:
# --------------------------------------------------------
# 版权声明：本文为CSDN博主「Zzzzzzzzzzzaa2」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/Xzike/article/details/123561409
# --------------------------------------------------------
# async def async_run(func):
#     sem = asyncio.Semaphore(10)
#     async with sem:
#         # work with shared resourse
#         func()
# import asyncio
# import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - |%(levelname)s| - %(message)s')

# async def func(x):
#     logging.info(1)
#     await asyncio.sleep(x)
#     logging.info(2)
#     return f'返回值{x}'

# async def main():
#     print('main start!')
#     task_list = [
#         asyncio.create_task(func(2),name = 'f1'),
#         asyncio.create_task(func(5),name = 'f2')
#     ]
#     print('main end!')

#     #写法1，使用asyncio.wait
#     # done,pending = await asyncio.wait(task_list,timeout = None)
#     # print(done)
#     # 此处打印的是一个Task finished对象的集合

#     #写法2，使用asyncio.gather，asyncio.gather依照协程执行的先后顺序来返回一个列表
#     # t = await asyncio.gather(*task_list)
#     # print(t)
#     # 此处打印：['返回值2', '返回值5']
# asyncio.run(main())


##############################################################################
#
# Based on:
# --------------------------------------------------------
# 原文链接：# https://www.cnblogs.com/swindler/p/17407141.html
# --------------------------------------------------------


async def asyncio_pool_run(func, params_list, max_workers=None):
    loop = asyncio.get_running_loop()
    tasks = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for params in params_list:
            tasks.append(loop.run_in_executor(executor, func, params))

        # Or we can just use the method asyncio.gather(*tasks)
        for done in asyncio.as_completed(tasks):
            result = await done
