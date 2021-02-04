import torch


def calculate_mean_std(data, eps=1e-5):  # 计算标准差、方差
    # eps用来防止零除
    size = data.size()
    assert (len(size) == 4)
    N, C = size[:2]
    data_std = (data.view(N, C, -1).var(dim=2) + eps).sqrt().view(N, C, 1, 1)
    data_mean = data.view(N, C, -1).mean(dim=2).mean().view(N, C, 1, 1)
    return data_mean, data_std


def adaptive_instance_normalization(content, style):
    assert (content.size()[:2] == style.size()[:2])
    size = content.size()
    style_mean, style_std = calc_mean_std(style)
    content_mean, content_std = calc_mean_std(content)

    normalized_feat = (content - content_mean.expand(
        size)) / content_std.expand(size)
    return normalized * style_std.expand(size) + style_mean.expand(size)
