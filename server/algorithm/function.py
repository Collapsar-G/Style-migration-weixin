#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/5 10:00

"""工具人"""

__author__ = 'Collapsar-G'

import torch


def calc_mean_std(feat, eps=1e-5):  # 计算标准差、均方差
    # eps 用来防止零除
    size = feat.size()
    assert (len(size) == 4)
    N, C = size[:2]
    feat_var = feat.view(N, C, -1).var(dim=2) + eps
    feat_std = feat_var.sqrt().view(N, C, 1, 1)
    feat_mean = feat.view(N, C, -1).mean(dim=2).view(N, C, 1, 1)
    return feat_mean, feat_std


def _mat_sqrt(x):
    U, D, V = torch.svd(x)  # SVD奇异值分解
    return torch.mm(torch.mm(U, D.pow(0.5).diag()), V.t())  # 对特征值开根号


def _calc_feat_flatten_mean_std(feat):
    # 特殊版本的均值方差计算，没有N这个维度 (C, H, W)
    assert (feat.size()[0] == 3)  # 所以assertion变了，这里要求C==3，也就是必须RGB三通道
    assert (isinstance(feat, torch.FloatTensor))  # 检查是否为浮点数tensor
    feat_flatten = feat.view(3, -1)  # 拉平
    mean = feat_flatten.mean(dim=-1, keepdim=True)
    std = feat_flatten.std(dim=-1, keepdim=True)  # 保存维度情况的计算均值和标准差（所以是3维）
    return feat_flatten, mean, std


def adaptive_instance_normalization(content_feat, style_feat):
    assert (content_feat.size()[:2] == style_feat.size()[:2])
    size = content_feat.size()
    style_mean, style_std = calc_mean_std(style_feat)
    content_mean, content_std = calc_mean_std(content_feat)

    normalized_feat = (content_feat - content_mean.expand(
        size)) / content_std.expand(size)
    return normalized_feat * style_std.expand(size) + style_mean.expand(size)


def coral(source, target):
    # 假定输入是三维的 (C, H, W)
    # 变量名带f的是flatten之后的意思

    source_f, source_f_mean, source_f_std = _calc_feat_flatten_mean_std(source)
    # 利用上面那个函数求拉平数据和均值标准差
    source_f_norm = (source_f - source_f_mean.expand_as(
        source_f)) / source_f_std.expand_as(source_f)
    source_f_cov_eye = \
        torch.mm(source_f_norm, source_f_norm.t()) + torch.eye(3)

    target_f, target_f_mean, target_f_std = _calc_feat_flatten_mean_std(target)
    target_f_norm = (target_f - target_f_mean.expand_as(
        target_f)) / target_f_std.expand_as(target_f)
    target_f_cov_eye = \
        torch.mm(target_f_norm, target_f_norm.t()) + torch.eye(3)

    source_f_norm_transfer = torch.mm(
        _mat_sqrt(target_f_cov_eye),
        torch.mm(torch.inverse(_mat_sqrt(source_f_cov_eye)),
                 source_f_norm)
    )

    source_f_transfer = source_f_norm_transfer * \
                        target_f_std.expand_as(source_f_norm) + \
                        target_f_mean.expand_as(source_f_norm)

    return source_f_transfer.view(source.size())
