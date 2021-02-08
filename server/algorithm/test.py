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
    vgg_path = 'algorithm/models/vgg_normalised.pth'
    decoder_path = 'algorithm/models/decoder.pth'
    # vgg_path = './models/vgg_normalised.pth'
    # decoder_path = './models/decoder.pth'
    content_dir = ''
    style_dir = ''
    content_size = 512  # New (minimum) size for the content image, keeping the original size if set to 0
    style_size = 512  # New (minimum) size for the style image, keeping the original size if set to 0
    save_ext = '.jpg'  # The extension name of the output image
    # output = 'output'  # Directory to save the output image(s)
    style_interpolation_weights = ''  # The weight for blending the style of multiple style images
    do_interpolation = True
    crop = True

    do_interpolation = False

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    output_dir = Path(output)
    output_dir.mkdir(exist_ok=True, parents=True)

    # Either --content or --contentDir should be given.
    assert (content or content_dir)
    if content:
        content_paths = [Path(content)]
    else:
        content_dir = Path(content_dir)
        content_paths = [f for f in content_dir.glob('*')]

    # Either --style or --styleDir should be given.
    assert (style or style_dir)
    if style:
        style_paths = style.split(',')
        if len(style_paths) == 1:
            style_paths = [Path(style)]
        else:
            do_interpolation = True
            assert (style_interpolation_weights != ''), \
                'Please specify interpolation weights'
            weights = [int(i) for i in style_interpolation_weights.split(',')]
            interpolation_weights = [w / sum(weights) for w in weights]
    else:
        style_dir = Path(style_dir)
        style_paths = [f for f in style_dir.glob('*')]

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
        if do_interpolation:  # one content image, N style image
            style = torch.stack([style_tf(Image.open(str(p))) for p in style_paths])
            content = content_tf(Image.open(str(content_path))) \
                .unsqueeze(0).expand_as(style)
            style = style.to(device)
            content = content.to(device)
            with torch.no_grad():
                output = style_transfer(vgg, decoder, content, style,
                                        alpha, interpolation_weights)
            output = output.cpu()
            output_name = output_dir / '{:s}_stylized_{:s}_alpha_{:s}_preserve_color_{:s}{:s}'.format(
                content_path.stem, style_path.stem, str(alpha), str(preserve_color), save_ext)
            save_image(output, str(output_name))

        else:  # process one content and one style
            for style_path in style_paths:
                content = content_tf(Image.open(str(content_path)))
                style = style_tf(Image.open(str(style_path)))
                if preserve_color:
                    style = coral(style, content)
                style = style.to(device).unsqueeze(0)
                content = content.to(device).unsqueeze(0)
                with torch.no_grad():
                    output = style_transfer(vgg, decoder, content, style,
                                            alpha)
                output = output.cpu()

                output_name = output_dir / '{:s}_stylized_{:s}_alpha_{:s}_preserve_color_{:s}{:s}'.format(
                    content_path.stem, style_path.stem, str(alpha), str(preserve_color), save_ext)
                save_image(output, str(output_name))
        return output_name


if __name__ == '__main__':
    img01 = cv2.imread(str(using_model('./input/content/sh1.jpg', './input/style_in/qjssh.jpeg', 1.0, False)))
    img_medianBlur = cv2.medianBlur(img01, 3)
    cv2.imshow('1', img_medianBlur)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
