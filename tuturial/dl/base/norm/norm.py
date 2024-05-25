# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

"""
手撕NORM层.

分为LN,BN,GN,IN, LLM是RMS NORM

发现比较好的博客：
1. https://blog.csdn.net/SugerOO/article/details/130029642
"""
from tuturial.dl.base.norm.rmsnorm import RMSNorm

import numpy as np
import torch
from torch.nn import BatchNorm2d, GroupNorm, InstanceNorm2d, LayerNorm


class MyBN:
    def __init__(self, dim, momentum=0.1, mode="train"):
        self.run_mean = np.zeros(shape=(dim,))
        self.run_var = np.ones(shape=(dim,))
        self.momentum = momentum
        self.eps = 1e-5
        self.mode = mode

    def __call__(self, input_):
        if self.mode == "train":
            # 计算均值方差
            mean = np.mean(input_, axis=(0, 2, 3))
            var = np.mean(
                (input_ - mean[None, :, None, None]) ** 2, axis=(0, 2, 3)
            )  # 次序: [None,:,None,None]

            # 滑动计算, 由于这里没有多轮循环，是用不到的
            self.run_mean = self.momentum * mean + self.run_mean * (
                1 - self.momentum
            )
            self.run_var = self.momentum * var + self.run_var * (
                1 - self.momentum
            )
        else:
            mean = self.run_mean  # 有偏均值方差，但是train模式下是无偏的
            var = self.run_var

        return (input_ - mean[None, :, None, None]) / (
            np.sqrt(var)[None, :, None, None] + self.eps
        )


class MyLN:
    def __init__(self) -> None:
        self.eps = 1e-5

    def __call__(self, input_):
        mean = np.mean(input_, axis=(1, 2, 3))
        var = np.mean(
            (input_ - mean[:, None, None, None]) ** 2, axis=(1, 2, 3)
        )
        return (input_ - mean[:, None, None, None]) / (
            np.sqrt(var)[:, None, None, None] + self.eps
        )


class MyIN:
    def __init__(self):
        self.eps = 1e-5

    def __call__(self, input_):
        mean = np.mean(input_, axis=(2, 3))
        var = np.mean((input_ - mean[:, :, None, None]) ** 2, axis=(2, 3))
        return (input_ - mean[:, :, None, None]) / (
            np.sqrt(var)[:, :, None, None] + self.eps
        )


class MyGN:
    def __init__(self, group_num=4, channel_input=16, mode="parallel"):
        self.group_num = group_num
        self.channel_input = channel_input
        assert channel_input // group_num
        self.grp_elm_num = channel_input // group_num

        assert mode in ["parallel", "loop"]
        self.mode = mode
        self.eps = 1e-5

    def __call__(self, input_):
        return getattr(self, f"forward_{self.mode}")(input_)

    def forward_parallel(self, input_):
        # https://arxiv.org/pdf/1803.08494
        b, c, h, w = input_.shape
        input_grps = input_.reshape(b, self.group_num, -1, h, w)
        mean = np.mean(input_grps, axis=(2, 3, 4))
        var = np.mean(
            (input_grps - mean[:, :, None, None, None]) ** 2, axis=(2, 3, 4)
        )
        out = (input_grps - mean[:, :, None, None, None]) / (
            np.sqrt(var)[:, :, None, None, None] + self.eps
        )
        out = out.reshape(input_.shape)
        return out

    def forward_loop(self, input_):
        input_grps = np.split(input_, self.group_num, axis=1)
        out = np.zeros_like(input_)
        for grpi, inp_ in enumerate(input_grps):
            mean = np.mean(inp_, axis=(1, 2, 3))
            var = np.mean(
                (inp_ - mean[:, None, None, None]) ** 2, axis=(1, 2, 3)
            )

            out[
                :,
                grpi * self.grp_elm_num : (grpi + 1) * self.grp_elm_num,
                :,
                :,
            ] = (inp_ - mean[:, None, None, None]) / (
                np.sqrt(var)[:, None, None, None] + self.eps
            )
        return out


class MyRMSNorm:
    """MyRMSNorm.

    https://github.com/bzhangGo/rmsnorm

    As RMSNorm does not consider the mean of the inputs,
    it's not re-centering invariant.
    This is the main difference compared to LayerNorm.

    gi set to 1.
    """

    def __init__(self):
        self.eps = 1e-5
        self.gi = 1

    def __call__(self, input_):
        rms = np.sqrt(np.mean(input_ ** 2, (1, 2, 3)))
        return input_ / (rms[:, None, None, None] + self.eps)


if __name__ == "__main__":
    bs = 2
    c = 16
    h, w = 128, 1

    # BN初始化
    bn_pt = BatchNorm2d(c, affine=False)
    bn_np = MyBN(c)

    # LN初始化
    ln_pt = LayerNorm([c, h, w], elementwise_affine=False)
    ln_np = MyLN()

    # IN初始化
    in_pt = InstanceNorm2d(c, affine=False)
    in_np = MyIN()

    # GN初始化
    group_num = 2
    assert c // group_num, "c should be .."
    gn_pt = GroupNorm(
        group_num, c, affine=False
    )  # Separate 16 channels into 4 groups
    gn_np = MyGN(group_num=group_num, channel_input=c)

    # RMS初始化
    rms_pt = RMSNorm(d=1, eps=1e-5)  # 不支持BCHW
    rms_pt = None
    rms_np = MyRMSNorm()

    # 选择具体的norm形式
    norm_pt = bn_pt
    norm_np = bn_np
    step_num = 10

    norm_pt = ln_pt
    norm_np = ln_np
    step_num = 1

    norm_pt = in_pt
    norm_np = in_np
    step_num = 1

    norm_pt = gn_pt
    norm_np = gn_np
    step_num = 1

    norm_pt = rms_pt
    norm_np = rms_np
    step_num = 1

    for step in range(step_num):
        print("=" * 50)
        print(f"step: {step}")
        input_ = np.random.rand(bs, c, h, w).astype(np.float32)  # BCHW
        input_pt = torch.from_numpy(input_)

        # 手写BN
        if norm_pt is not None:
            out_pt = norm_pt(input_pt)
            print("out_bn_pt[0][0][0][0:10]: ", out_pt[0][0][0][0:10])

        out_np = norm_np(input_)
        print("out_np[0][0][0][0:10]: ", out_np[0][0][0][0:10])

        if norm_pt is not None:
            assert np.allclose(
                out_pt.detach().numpy(), out_np, atol=1e-4
            ), "fail"
