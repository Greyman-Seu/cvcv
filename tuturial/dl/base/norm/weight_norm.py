# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import numpy as np
import torch
from torch import nn
from torch.nn.utils import weight_norm

if __name__ == "__main__":
    # input
    input_ = np.random.rand(2, 3, 16).astype(np.float32)  # BCL
    input_pt = torch.from_numpy(input_)
    # 初始化WN
    linear_layer = nn.Linear(16, 40, bias=False)
    linear_layer_wn = weight_norm(linear_layer, name="weight", dim=0)

    wn_output = linear_layer_wn(input_pt)
    print(wn_output.shape)

    # 获取linear权重
    weight_np = linear_layer.weight.detach().numpy()  # (40, 16)
    # 归一化在input维度
    weight_v = weight_np / np.linalg.norm(weight_np, axis=1, keepdims=True)
    weight_g = np.linalg.norm(weight_np, axis=1)

    out_np = input_pt @ weight_v.T  # 2,3,40
    out_np = out_np * weight_g[None, None, :]
    print(out_np.shape)

    np.allclose(wn_output.detach().numpy(), out_np, atol=1e-4), "fail"
