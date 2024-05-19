# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__all__ = []


###  使用说明
# 最常使用apply_async
# io过于密集，使用协程


##############################################################################
#
# Based on:  https://blog.csdn.net/BobYuan888/article/details/109266020
# 版权声明：本文为CSDN博主「忘尘~」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# --------------------------------------------------------
# Python进程池multiprocessing.Pool八个函数对比:
# 1. apply 和 apply_async 一次执行一个任务，但 apply_async 可以异步执行，因而也可以实现并发。
# 2. map 和 map_async 与 apply 和 apply_async 的区别是可以并发执行任务。
# 3. starmap 和 starmap_async 与 map 和 map_async 的区别是，starmap 和 starmap_async 可以传入多个参数。
# 4. imap 和 imap_unordered 与 map_async 同样是异步，区别是:
#    map_async生成子进程时使用的是list，而imap和 imap_unordered则是Iterable，map_async效率略高，而imap和 imap_unordered内存消耗显著的小。
#    在处理结果上，imap 和 imap_unordered 可以尽快返回一个Iterable的结果，而  （重要)*map_async则需要等待全部Task执行完毕，返回list。*
# 5. 而imap 和 imap_unordered 的区别是：imap 和 map_async一样，都按顺序等待Task的执行结果，而imap_unordered则不必。 imap_unordered返回的Iterable，会优先迭代到先执行完成的Task。 不理解的看最下面的一组例子。
# --------------------------------------------------------

##############################################################################
#
# Based on:  AI
# --------------------------------------------------------
# 复杂使用apply_async，简单元素处理使用map
# map_async和apply_async都是Python的multiprocessing模块中的函数，用于在多个进程中并行执行任务，但它们的功能和使用场景有所不同。
# map_async函数的作用是对一个可迭代的对象中的每个元素执行一个指定的函数，并将结果以列表的形式返回。它接受一个函数和一个可迭代的对象作为输入，并返回一个AsyncResult对象。map_async可以并发执行任务，但并不支持向函数传递参数。对于每个元素，map_async会将其作为参数传递给指定的函数，并等待函数执行完成后将结果合并为一个列表返回。
# apply_async函数的作用是异步地在多个进程中执行一个指定的函数，并返回一个ApplyResult对象。与map_async不同，apply_async支持向函数传递参数，并且可以指定关键字参数。它接受一个函数和零个或多个参数作为输入，并返回一个ApplyResult对象。在任务完成后，可以通过调用ApplyResult对象的get方法获取函数返回值。
# 总的来说，map_async和apply_async都用于在多个进程中并行执行任务，但map_async更适用于对一个可迭代的对象中的每个元素执行相同的函数，而apply_async更适用于执行复杂的并行任务，并支持向函数传递参数和指定关键字参数。
# --------------------------------------------------------


##############################################################################
#
# Based on:  https://docs.python.org/zh-cn/3/library/multiprocessing.html#module-multiprocessing.pool
# --------------------------------------------------------
# apply(func[, args[, kwds]])
# 使用 args 参数以及 kwds 命名参数调用 func , 它会返回结果前阻塞。这种情况下，apply_async() 更适合并行化工作。另外 func 只会在一个进程池中的一个工作进程中执行。

# apply_async(func[, args[, kwds[, callback[, error_callback]]]])
# apply() 方法的一个变种，返回一个 AsyncResult 对象。
# 如果指定了 callback , 它必须是一个接受单个参数的可调用对象。当执行成功时， callback 会被用于处理执行后的返回结果，否则，调用 error_callback 。
# 如果指定了 error_callback , 它必须是一个接受单个参数的可调用对象。当目标函数执行失败时， 会将抛出的异常对象作为参数传递给 error_callback 执行。
# 回调函数应该立即执行完成，否则会阻塞负责处理结果的线程。

# map(func, iterable[, chunksize])
# 内置 map() 函数的并行版本 (但它只支持一个 iterable 参数，对于多个可迭代对象请参阅 starmap())。 它会保持阻塞直到获得结果。
# 这个方法会将可迭代对象分割为许多块，然后提交给进程池。可以将 chunksize 设置为一个正整数从而（近似）指定每个块的大小可以。
# 注意对于很长的迭代对象，可能消耗很多内存。可以考虑使用 imap() 或 imap_unordered() 并且显式指定 chunksize 以提升效率。

# map_async(func, iterable[, chunksize[, callback[, error_callback]]])
# map() 方法的一个变种，返回一个 AsyncResult 对象。
# 如果指定了 callback , 它必须是一个接受单个参数的可调用对象。当执行成功时， callback 会被用于处理执行后的返回结果，否则，调用 error_callback 。
# 如果指定了 error_callback , 它必须是一个接受单个参数的可调用对象。当目标函数执行失败时， 会将抛出的异常对象作为参数传递给 error_callback 执行。
# 回调函数应该立即执行完成，否则会阻塞负责处理结果的线程。

# imap(func, iterable[, chunksize])
# map() 的延迟执行版本。
# chunksize 参数的作用和 map() 方法的一样。对于很长的迭代器，给 chunksize 设置一个很大的值会比默认值 1 极大 地加快执行速度。
# 同样，如果 chunksize 是 1 , 那么 imap() 方法所返回的迭代器的 next() 方法拥有一个可选的 timeout 参数： 如果无法在 timeout 秒内执行得到结果，则 next(timeout) 会抛出 multiprocessing.TimeoutError 异常。

# imap_unordered(func, iterable[, chunksize])
# 和 imap() 相同，只不过通过迭代器返回的结果是任意的。（当进程池中只有一个工作进程的时候，返回结果的顺序才能认为是"有序"的）
# starmap(func, iterable[, chunksize])
# 和 map() 类似，不过 iterable 中的每一项会被解包再作为函数参数。
# 比如可迭代对象 [(1,2), (3, 4)] 会转化为等价于 [func(1,2), func(3,4)] 的调用。

# 3.3 新版功能.
# starmap_async(func, iterable[, chunksize[, callback[, error_callback]]])
# 相当于 starmap() 与 map_async() 的结合，迭代 iterable 的每一项，解包作为 func 的参数并执行，返回用于获取结果的对象。
# 3.3 新版功能.
# close()
# 阻止后续任务提交到进程池，当所有任务执行完成后，工作进程会退出。
# terminate()
# 不必等待未完成的任务，立即停止工作进程。当进程池对象被垃圾回收时，会立即调用 terminate()。
# --------------------------------------------------------
