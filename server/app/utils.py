#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 10:12

'永远的工具人'

__author__ = 'Judgement'

import base64
import os
import re
import time

from PIL import Image
from io import BytesIO


def base64_to_imagefile(image_base64: str, save_path: str):
    """
    把base64图片保存为文件，
    @param base64: 图片编码
    @param save_path: 不带文件名的保存路径
    @return 图片文件地址
    """
    img_base64 = image_base64.split(';base64,')[1]
    img = base64.b64decode(img_base64)
    # pattern = re.compile(r'data:image/(.*?);base64')
    # img_type = pattern.search(image_base64).group(1)
    # if img_type == 'jpeg':
    #     img_type = 'jpg'
    img_type = 'jpg'

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    t = int(time.time())
    img_path = f"{save_path}/{t}.{img_type}"

    im = Image.open(BytesIO(img))
    im.convert('RGB').save(img_path)
    return img_path
