# -*- encoding: utf-8 -*-
# Copyright (c) TenStep[yangkun.zhu]. All rights reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import random
import numpy as np

try:
    import torch
    import torch.backends.cudnn as cudnn
except:
    torch = None

__all__ = []


def set_seed(seed=3407):
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def set_torch_seed(seed=3407):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    cudnn.deterministic = True
    cudnn.benchmark = False


def seed_everything(seed=3407):
    set_seed(seed)
    if torch is not None:
        set_torch_seed(seed)
