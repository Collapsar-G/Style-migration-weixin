#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/25 17:42

'关于图片上传的api'

__author__ = 'Judgement'

import os
import time
import traceback

from flask import Blueprint, request, jsonify, url_for, session

from app import utils
from algorithm.test import using_model
from app.database.models import db, Image, Transfer

show = Blueprint('show', __name__)

path = 'static/image/show'

# HOST = 'http://127.0.0.1:3268'


# HOST = 'http://39.105.76.87:3268'
HOST = 'https://xcx.collapsar.online'


@show.route('/show_all/', methods=['POST'])
def show_all():
    files = os.listdir(path)
    images = []
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            images.append(HOST+'/'+path + '/' + str(file))
    return jsonify(code=200, msg='success', data=images, num=len(images))
