#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/25 17:42

"""图片展示api"""

__author__ = 'Collapsar-G'

import os
import time
import traceback

from flask import Blueprint, request, jsonify, url_for, session

from app import utils
from algorithm.test import using_model
from app.database.models import db, Image, Transfer
import json
show = Blueprint('show', __name__)

path = 'static/image/show'

# HOST = 'http://127.0.0.1:3268'


# HOST = 'http://39.105.76.87:3268'
# HOST = 'https://xcx.collapsar.online'


@show.route('/show_all/', methods=['POST'])
def show_all():
    try:
        f = open('./static/json/show.json', 'r')
        content = f.read()
        a = json.loads(content)
        # print(a)
    except:
        return jsonify(code=400, msg='读取文件错误')
    return jsonify(code=200, msg='success', data=a)
