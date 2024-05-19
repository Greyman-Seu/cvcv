# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pickle

__all__=[
    "serialize_object",
    "deserialize_object",
]

############################################################################## 
#  
# Based on:  CHATGPT
# -------------------------------------------------------- 
# # 定义一个Python对象
# class MyClass:
#     def __init__(self, name):
#         self.name = name

# # 创建一个对象实例
# my_obj = MyClass('Example')

# # 序列化对象到磁盘
# serialize_object(my_obj, 'serialized_object.pkl')

# # 从磁盘反序列化对象
# deserialized_obj = deserialize_object('serialized_object.pkl')

# # 打印反序列化后的对象属性
# print(deserialized_obj.name)
# --------------------------------------------------------

# 序列化对象到磁盘
def serialize_object(obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)
    return True

# 从磁盘反序列化对象
def deserialize_object(filename):
    with open(filename, 'rb') as file:
        obj = pickle.load(file)
        return obj



