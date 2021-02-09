#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/6 10:00

"""url测试文件"""

__author__ = 'Collapsar-G'

import requests
import simplejson
import base64
import numpy as np
import cv2


# 首先将图片读入
# 由于要发送json，所以需要对byte进行str解码
def getByte(path):
    with open(path, 'rb') as f:
        img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode('ascii')
    return img_str


if __name__ == '__main__':
    appid = "wx7330267cab93fa97"
    secret = "d2d27f80db202377fbb8ca9d49eab458"
    code = "0012Yo0w3nV9PV2xeu2w3KJjoW12Yo0h"
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'.format(
        appid=appid, secret=secret, code=code)
    res = requests.get(url)
    print(res.text)
    openid = res.json().get('openid')
    session_key = res.json().get('session_key')
    print(openid,session_key)