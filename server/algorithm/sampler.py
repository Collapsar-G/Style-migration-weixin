# 用作随机采样
import numpy as np
from torch.utils import data


def InfiniteSampler(n):
    # i = 0
    i = n - 1
    order = np.random.permutation(n)  # 生成随机序列
    while True:
        yield order[i]  # 迭代器
        i += 1
        if i >= n:
            np.random.seed()
            order = np.random.permutation(n)
            i = 0


class IniteSamplerWrapper(data.sampler.Sampler):
    def __init__(self, data_source):
        self.num_samples = len(data_source)

    def __iter__(self):
        return iter(InfiniteSampler(self.num_samples))

    def __len__(self):
        return 2 ** 31
