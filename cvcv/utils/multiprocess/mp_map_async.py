# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import multiprocessing

__all__=[
    "pool_map_async_example",
    "pool_map_async_log_example"
]


def pool_map_async_example(worker_func,params):
    """pool_map_async
    
    Usage::
        pool_size = 8
        with multiprocessing.Pool(pool_size) as p:
            error_tensors = p.map_async(
                partial(_track_sequence, model_path=model_path), 
                zip(input_paths, output_paths)).get()
                        |
                        |-> list

        error_tensors = [t for t in error_tensors if t is not None]

        apply_async 与 map_async 差异

        # 定义一个类，用于计算平方
        class SquareCalculator:
            def square(self, x):
                return x ** 2

        if __name__ == '__main__':
            # 创建一个包含多个进程的进程池
            pool = multiprocessing.Pool()

            # 要处理的数据列表
            data = [1, 2, 3, 4, 5]

            # 创建SquareCalculator对象
            calculator = SquareCalculator()

            # 使用apply_async函数并行计算平方
            results = [pool.apply_async(calculator.square, (x,)) for x in data]

            # 等待所有任务完成并获取结果列表
            squared_data = [result.get() for result in results]

            # 打印结果
            print(squared_data)


            import multiprocessing

            # 定义一个函数，用于计算平方
            def square(x):
                return x ** 2

            if __name__ == '__main__':
                # 创建一个包含多个进程的进程池
                pool = multiprocessing.Pool()

                # 要处理的数据列表
                data = [1, 2, 3, 4, 5]

                # 使用map_async函数并行计算平方
                result = pool.map_async(square, data)

                # 等待所有任务完成
                result.wait()

                # 获取结果列表
                squared_data = result.get()

                # 打印结果
                print(squared_data)

    """
    pool_size = 8
    with multiprocessing.Pool(pool_size) as p:
        error_tensors = p.map_async(
            worker_func,  params).get()
    error_tensors = [t for t in error_tensors if t is not None]


def pool_map_async_log_example(worker_func,params):
    return """
    import multiprocessing
    import time

    def worker_func(args):
        # 实际的任务处理逻辑
        dataset, index = args
        # ...
        # 更新计数器
        progress_counter.value += 1

    def print_progress(progress_counter, total_progress):
        while progress_counter.value < total_progress:
            progress = progress_counter.value
            print(f"总进度：{progress}/{total_progress}")
            time.sleep(1)  # 每秒钟打印一次进度

    if __name__ == '__main__':
        pool_size = 8
        len_dataset = 100
        progress_counter = multiprocessing.Manager().Value('i', 0)  # 创建共享的计数器

        with multiprocessing.Pool(pool_size) as p:
            results = p.map_async(worker_func, zip([dataset] * len(range(0, len_dataset, 10)), list(range(0, len_dataset, 10))))

            # 启动进程打印进度
            total_progress = len(range(0, len_dataset, 10))
            progress_process = multiprocessing.Process(target=print_progress, args=(progress_counter, total_progress))
            progress_process.start()

            # 等待任务完成
            results.wait()

            # 结束进度打印进程
            progress_process.terminate()

            # 获取结果列表
            data_list = results.get()

            # 过滤空结果
            data_list = [t for t in data_list if t is not None]
    """
   