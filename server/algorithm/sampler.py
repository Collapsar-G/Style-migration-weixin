# 用作随机采样
import numpy as np
from torch.utils import data


def init_Sampler(n):
    i = n - 1
    order = np.random.permutation(n)  # 生成随机序列
    while True:  # 循环
        yield order[i]  # 迭代器
        i += 1
        if i >= n:
            np.random.seed()  # 随机数种子
            order = np.random.permutation(n)
            i = 0


class InitSamplerWrapper(data.sampler.Sampler):
    def __init__(self, data_source):
        super().__init__(data_source)
        self.num_samples = len(data_source)

    def __iter__(self):
        return iter(init_Sampler(self.num_samples))

    def __len__(self):
        return 2 ** 31
