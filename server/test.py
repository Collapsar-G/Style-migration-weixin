#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 1:15

'commit'

__author__ = 'Judgement'

import base64
import os
import time

from flask import Blueprint, request, jsonify

from algorithm.test import using_model

test = Blueprint('test', __name__)
basepath = os.path.abspath(os.path.dirname(__file__))


@test.route('/test', methods=['GET'])
def t1():
    return '1'


@test.route('/getImg', methods=['POST'])
def getImg():
    param = request.form.to_dict()
    img_base64 = param['image'].split(';base64,')[1]
    img_base64 = base64.b64decode(img_base64)
    input_img_url = save_image_file('static/images/input', img_base64)
    output_img_url = using_model(input_img_url, "F:\style.jpg", 0, True)
    print(output_img_url)
    return jsonify(url=output_img_url, code=200)


@test.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('image')
    if file is None:
        return jsonify(code=400)
    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)

    new_name = str(int(time.time())) + '.' + filename.rsplit('.', 1)[-1]
    save_path = basepath + '/static/image/input/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file.save(save_path + new_name)

    # 返回地址
    host = 'http://127.0.0.1:3268'
    image_url = host + '/static/image/input/' + new_name
    return jsonify(url=image_url, code=200)

def save_image_file(image_url, data):
    if not os.path.exists(image_url):
        os.makedirs(image_url)
    t = int(time.time())
    image_url = f"{image_url}/{t}.jpg"
    with open(image_url, 'wb') as f:
        f.write(data)
    return image_url

def get_imageb64_from_file(image_url):
    with open(image_url, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
    return 'data:image/jpeg;base64,%s' % s
