#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/5 20:00

"""算法调用文件"""

__author__ = 'Collapsar-G'

import argparse
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.utils import save_image
import cv2
from algorithm import net
from algorithm.function import adaptive_instance_normalization, coral
# import net
# from function import adaptive_instance_normalization, coral
import numpy as np


def test_transform(size, crop):
    transform_list = []
    if size != 0:
        transform_list.append(transforms.Resize(size))
    if crop:
        transform_list.append(transforms.CenterCrop(size))
    transform_list.append(transforms.ToTensor())
    transform = transforms.Compose(transform_list)
    return transform


def style_transfer(vgg, decoder, content, style, alpha=1.0,
                   interpolation_weights=None):
    assert (0.0 <= alpha <= 1.0)
    content_f = vgg(content)
    style_f = vgg(style)
    if interpolation_weights:
        _, C, H, W = content_f.size()
        feat = torch.FloatTensor(1, C, H, W).zero_().to(device)
        base_feat = adaptive_instance_normalization(content_f, style_f)
        for i, w in enumerate(interpolation_weights):
            feat = feat + w * base_feat[i:i + 1]
        content_f = content_f[0:1]
    else:
        feat = adaptive_instance_normalization(content_f, style_f)
    feat = feat * alpha + content_f * (1 - alpha)
    return decoder(feat)


def using_model(content, style, alpha, preserve_color=False, output='static/image/output'):
    global output_name
    vgg_path = 'algorithm/models/vgg_normalised.pth'
    decoder_path = 'algorithm/models/decoder.pth'
    # vgg_path = './models/vgg_normalised.pth'
    # decoder_path = './models/decoder.pth'

    content_size = 512  # New (minimum) size for the content image, keeping the original size if set to 0
    style_size = 512  # New (minimum) size for the style image, keeping the original size if set to 0
    save_ext = '.jpg'  # The extension name of the output image
    crop = True

    do_interpolation = False

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    output_dir = Path(output)
    output_dir.mkdir(exist_ok=True, parents=True)

    # Either --content  should be given.
    # assert (content or content_dir)
    assert content

    content_paths = [Path(content)]
    assert style

    style_paths = [Path(style)]

    decoder = net.decoder
    vgg = net.vgg

    decoder.eval()
    vgg.eval()

    decoder.load_state_dict(torch.load(decoder_path))
    vgg.load_state_dict(torch.load(Path(vgg_path)))
    vgg = nn.Sequential(*list(vgg.children())[:31])

    vgg.to(device)
    decoder.to(device)

    content_tf = test_transform(content_size, crop)
    style_tf = test_transform(style_size, crop)

    for content_path in content_paths:
        for style_path in style_paths:
            img_content = Image.open(str(content_path))
            (h, w) = img_content.size
            size_image = h
            if w > h:
                size_image = w
            img_content_resize = img_content.resize((size_image, size_image))
            content = content_tf(img_content_resize)
            style = style_tf(Image.open(str(style_path)))
            if preserve_color:
                style = coral(style, content)
            style = style.to(device).unsqueeze(0)
            content = content.to(device).unsqueeze(0)
            with torch.no_grad():
                output = style_transfer(vgg, decoder, content, style,
                                        alpha)
            output = output.cpu()
            output_resize = (transforms.ToPILImage()(output[0]).convert('RGB')).resize((h,w))
            # output_resize.show()
            # output_array = output.numpy()
            # output_resize = Image.fromarray(output_array[0][0]).resize((h,w))
            # output_array = torch.from_numpy(np.array(output_resize))
            output_name = output_dir / '{:s}_stylized_{:s}_alpha_{:s}_preserve_color_{:s}{:s}'.format(
                content_path.stem, style_path.stem, str(alpha), str(preserve_color), save_ext)
            # save_image(output, str(output_name))
            output_resize.save(str(output_name))
        return output_name


if __name__ == '__main__':
    img01 = cv2.imread(str(using_model('./input/content/flowers.jpg', './input/style_in/qjssh.jpeg', 1.0, False)))
    img_medianBlur = cv2.medianBlur(img01, 3)
    cv2.imshow('1', img_medianBlur)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
