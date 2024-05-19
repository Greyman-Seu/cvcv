# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

"""
手撕CONV层.

分为滑动窗和im2col两种,滑动窗以左上角为主
"""
import math

import numpy as np
import torch


def np_window_conv(img, kernel, bias, stride=1, padding=0):
    # 遍历输出
    bs, input_c, input_h, input_w = img.shape
    out_c, input_c_k, kernel_h, kernel_w = kernel.shape
    assert input_c == input_c_k, "img channel must be equ to kernel input size"
    out_h = (
        math.floor((input_h + 2 * padding - kernel_h) / stride) + 1
    )  # 默认都是正方的
    out_w = math.floor((input_w + 2 * padding - kernel_w) / stride) + 1

    # init out
    out = np.zeros(shape=(bs, out_c, out_h, out_w))
    # loop for out
    for bsi in range(bs):
        for owc in range(out_c):
            for ohi in range(out_h):
                for owj in range(out_w):
                    out[bsi, owc, ohi, owj] = bias[owc]

                    # loop for kernel
                    for kc in range(input_c):
                        for ki in range(kernel_h):
                            for kj in range(kernel_w):
                                # print(
                                #     "bsi,owc,ohi,owj,kc,ki,kj: ",
                                #     bsi,owc,ohi,owj, kc, ki, kj)
                                # print(
                                #     "bsi, kc, ohi+ki-padding, \
                                #     owj+kj-padding",bsi, kc,
                                #     ohi+ki-padding, owj+kj-padding)

                                # 计算输入图像中的实际位置
                                ih = ohi * stride + ki - padding
                                iw = owj * stride + kj - padding

                                # 检查位置是否在图像范围内
                                if (
                                    ih >= 0
                                    and ih < input_h
                                    and iw >= 0
                                    and iw < input_w
                                ):
                                    out[bsi, owc, ohi, owj] += (
                                        kernel[owc, kc, ki, kj]
                                        * img[bsi, kc, ih, iw]
                                    )
    return out


if __name__ == "__main__":

    img = np.random.randn(2, 3, 8, 8)  # BCHW
    bs, input_c = img.shape[:2]
    out_c = 10

    for kernel_size in [3, 5, 7]:
        for padding in [1, 2, 3]:
            for stride in [1, 2, 3]:
                # torch
                conv_op = torch.nn.Conv2d(
                    input_c,
                    out_c,
                    kernel_size,
                    stride=stride,
                    padding=padding,
                    bias=True,
                )
                out = conv_op(torch.from_numpy(img).to(dtype=torch.float32))
                print("torch output shape: ", out.shape)

                # get kernel size
                kernel = conv_op.weight.detach().numpy()
                bias = conv_op.bias.detach().numpy()
                print("torch kernel shape: ", kernel.shape)
                print("torch bias shape: ", bias.shape)

                # numpy conv
                out_np_window = np_window_conv(
                    img, kernel, bias, stride=stride, padding=padding
                )
                assert np.allclose(
                    out.detach().numpy(), out_np_window, atol=1e-6
                ), "fail"
