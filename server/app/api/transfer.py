#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 10:01

'关于图片上传的api'

__author__ = 'Judgement'

import os
import traceback

from flask import Blueprint, request, jsonify, url_for

from app import utils
from algorithm.test import using_model

transfer = Blueprint('transfer', __name__)
basepath = os.path.abspath(os.path.dirname(__file__))

INPUT_PATH = 'static/image/input'
STYLE_QLSSH_PATH = 'static/image/style/qlssh.jpg'
STYLE_QJSSH_PATH = 'static/image/style/qjssh.jpg'
HOST = '127.0.0.1:3268'


# HOST = '39.105.76.87:3268'
<<<<<<< HEAD:server/app/api/transfer.py
# HOST = 'https://xcx.collapsar.online:3268'

@transfer.route('/test')
def url():
    return url_for('transfer.url', _external=True)

=======
HOST = 'https://xcx.collapsar.online'
>>>>>>> bd43e0060355b64d69cd1a4d5c597e60e3897de0:server/api/transfer.py

@transfer.route('/style_qlssh_no', methods=['POST'])
def style_qlssh_no():
    """
    青山绿水图不保留原色
    @param image:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param alpha:参数
    @return code(200=正常返回，400=错误),url:图片地址
    """
    try:
        param = request.form.to_dict()
        img_base64 = param['image']
        alpha = float(param['alpha'])
        img_path = utils.base64_to_imagefile(img_base64, save_path=INPUT_PATH)
        output_img_url = using_model(img_path, STYLE_QLSSH_PATH, alpha, False)
        img_url = HOST + '/' + str(output_img_url)
        return jsonify(url=img_url, code=200)
    except Exception:
        traceback.print_exc()
        return jsonify(code=400)


@transfer.route('/style_qlssh_is', methods=['POST'])
def style_qlssh_is():
    """
    青山绿水图保留原色
    @param image:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param alpha:参数
    @return code(200=正常返回，400=错误),url:图片地址
    """
    try:
        param = request.form.to_dict()
        img_base64 = param['image']
        alpha = float(param['alpha'])
        img_path = utils.base64_to_imagefile(img_base64, save_path=INPUT_PATH)
        output_img_url = using_model(img_path, STYLE_QLSSH_PATH, alpha, True)
        img_url = HOST + '\\' + str(output_img_url)
        return jsonify(url=img_url, code=200)
    except Exception:
        traceback.print_exc()
        return jsonify(code=400)


@transfer.route('/style_qjssh_no', methods=['POST'])
def style_qjssh_no():
    """
    浅绛山水画不保留原色
    @param image:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param alpha:参数
    @return code(200=正常返回，400=错误),url:图片地址
    """
    try:
        param = request.form.to_dict()
        img_base64 = param['image']
        alpha = float(param['alpha'])
        img_path = utils.base64_to_imagefile(img_base64, save_path=INPUT_PATH)
        output_img_url = using_model(img_path, STYLE_QJSSH_PATH, alpha, False)
        img_url = HOST + '\\' + str(output_img_url)
        return jsonify(url=img_url, code=200)
    except Exception:
        traceback.print_exc()
        return jsonify(code=400)


@transfer.route('/style_qjssh_is', methods=['POST'])
def style_qjssh_is():
    """
    浅绛山水画不保留原色
    @param image:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param alpha:参数
    @return code(200=正常返回，400=错误),url:图片地址
    """
    try:
        param = request.form.to_dict()
        img_base64 = param['image']
        alpha = float(param['alpha'])
        img_path = utils.base64_to_imagefile(img_base64, save_path=INPUT_PATH)
        output_img_url = using_model(img_path, STYLE_QJSSH_PATH, alpha, True)
        img_url = HOST + '\\' + str(output_img_url)
        return jsonify(url=img_url, code=200)
    except Exception:
        traceback.print_exc()
        return jsonify(code=400)
