# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

"""
手撕CONV层.

分为滑动窗和im2col两种,im2col就是将图像索引成一个矩阵,直接和kernel矩阵矩阵乘
1. 先去把kernel转换为矩阵, (input)*(output)
2. 先padding,正向去看stride相对好懂
3. 按kernel元素循环, 在pad img找出来和空间ij元素有关的元素,此时没有拉平CHANNEL, 方便直接赋值
"""

import math

import numpy as np
import torch


def im2col(img, kernel_h, kernel_w, out_h, out_w, stride=1, padding=0):
    bs, input_c, input_h, input_w = img.shape

    # init col
    numel_singlelayer_kernel = kernel_h * kernel_w
    col = np.zeros(
        shape=(bs, numel_singlelayer_kernel * input_c, out_h * out_w)
    )

    # pad img
    img_pad = np.pad(
        img, ((0, 0), (0, 0), (padding, padding), (padding, padding))
    )

    for ki in range(kernel_h):
        for kj in range(kernel_w):
            # 取(out_h, out_w)sub图, 这里的赋值还是很巧妙
            img_sub = img_pad[
                :,
                :,
                ki : ki + stride * out_h : stride,
                kj : kj + stride * out_w : stride,
            ]  # bs, ic, out_h, out_w
            img_sub = img_sub.reshape(bs, input_c, -1)
            # 赋值
            col[
                :, ki * kernel_w + kj :: numel_singlelayer_kernel, :
            ] = img_sub  # bs, ks, subh* subw

    return col


def np_im2col_conv(img, kernel, bias, stride=1, padding=0):
    bs, input_c, input_h, input_w = img.shape
    out_c, input_c_k, kernel_h, kernel_w = kernel.shape
    assert (
        input_c == input_c_k
    ), "img channel must be equal to kernel input size"

    out_h = math.floor((input_h + 2 * padding - kernel_h) / stride) + 1
    out_w = math.floor((input_w + 2 * padding - kernel_w) / stride) + 1

    # step1: kernel2col
    kernel_col = kernel.reshape(
        out_c, -1
    )  # out_c, (input_c_k* kernel_h* kernel_w)-kernelsize

    # step2: im2col
    img_col = im2col(
        img, kernel_h, kernel_w, out_h, out_w, stride=stride, padding=padding
    )  # bs, kernelsize, output_h*w

    # step3: dot
    conv_out = kernel_col @ img_col.transpose(1, 0, 2).reshape(
        kernel_col.shape[1], -1
    )  # out_c, bs* output_h*w

    conv_out = conv_out.reshape(out_c, bs, out_h, out_w).transpose(1, 0, 2, 3)
    out = conv_out + bias[None, :, None, None]
    return out


if __name__ == "__main__":
    img = np.random.randn(2, 3, 8, 8)  # BCHW
    bs, input_c = img.shape[:2]
    out_c = 10

    for kernel_size in [3, 5, 7]:
        for padding in [0, 1, 2, 3]:
            for stride in [1, 2, 3]:
                # 使用torch的卷积操作
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

                # 获取kernel和bias
                kernel = conv_op.weight.detach().numpy()
                bias = conv_op.bias.detach().numpy()
                print("torch kernel shape: ", kernel.shape)
                print("torch bias shape: ", bias.shape)

                # numpy实现的im2col卷积操作
                out_np_im2col = np_im2col_conv(
                    img, kernel, bias, stride=stride, padding=padding
                )
                assert np.allclose(
                    out.detach().numpy(), out_np_im2col, atol=1e-6
                ), f"fail kernel_size{kernel_size}  \
                        padding{padding} stride{stride}"
                print("numpy im2col output shape: ", out_np_im2col.shape)
