# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.
"""
手撕DROPOUT.

dropout是核心的模型组件之一, 仿照集成学习提高模型能力, 但是劣势是训练和推理不一致。

droprate并不是一定丢弃0.2, 只是一个阈值概率, 实际每个样本丢失的状态时是随机的, 平均是丢失20%
"""

import numpy as np
import torch
import torch.nn.functional as F


def dropout(x_input, w1, b1, w2, b2, drop_rate=0.2, mode="train"):
    # (mlp relu dropout) * 2
    feat = np.maximum(0, np.dot(x_input, w1) + b1)
    if mode == "train":
        mask1 = np.random.binomial(1, p=1 - drop_rate, size=feat.shape)
        feat = feat * mask1 / (1 - drop_rate)
    out = np.maximum(0, np.dot(feat, w2) + b2)
    if mode == "train":
        mask2 = np.random.binomial(1, p=1 - drop_rate, size=out.shape)
        print(mask2)
        out = out * mask2 / (1 - drop_rate)
    return out


if __name__ == "__main__":
    bs = 5
    channels = [128, 64, 10]
    drop_rate = 0.2
    mode = "train"

    # input
    x_input = np.random.rand(bs, channels[0])  # 0-1

    # net parameter
    w1 = np.random.rand(channels[0], channels[1]) - 0.5
    b1 = np.random.rand(channels[1]) - 0.5

    w2 = np.random.rand(channels[1], channels[2]) - 0.5
    b2 = np.random.rand(channels[2]) - 0.5

    dropout(x_input, w1, b1, w2, b2, drop_rate=0.2, mode="train")

    print(
        F.dropout(
            input=torch.full((bs, 10), 0.5, dtype=torch.float32),
            p=0.5,
            training=True,
        )
    )
