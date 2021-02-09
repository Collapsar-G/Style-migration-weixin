#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 10:01

'关于图片上传的api'

__author__ = 'Judgement'

import os
import time
import traceback

from flask import Blueprint, request, jsonify, url_for, session

from app import utils
from algorithm.test import using_model
from app.database.models import db, Image, Transfer

transfer = Blueprint('transfer', __name__)
basepath = os.path.abspath(os.path.dirname(__file__))

INPUT_PATH = 'static/image/input'
STYLE_QLSSH_PATH = 'static/image/style/qlssh.jpg'
STYLE_QJSSH_PATH = 'static/image/style/qjssh.jpg'
# HOST = '127.0.0.1:3268'

# HOST = '39.105.76.87:3268'
HOST = 'https://xcx.collapsar.online'


@transfer.route('/test')
def url():
    return url_for('transfer.url', _external=True)


@transfer.route('/style_qlssh_no', methods=['POST'])
def style_qlssh_no():
    """
    青山绿水图不保留原色
    @param image:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param alpha:参数
    @param id:用户id，非必须
    @return code(200=正常返回，400=错误),url:图片地址
    """
    param = request.get_json()
    img_base64 = param.get('image')
    alpha = float(param.get('alpha'))
    user_id = param.get('id')
    if not all([img_base64, alpha]):
        return jsonify(code=400, msg='lack of parameters')

    img_path = utils.base64_to_imagefile(img_base64, save_path=INPUT_PATH)
    output_img_url = using_model(img_path, STYLE_QLSSH_PATH, alpha, False)
    img_url = HOST + '/' + str(output_img_url)
    print(img_url)
    if not user_id:
        return jsonify(url=img_url, code=200, msg='success without id')

    try:
        image = Image(url=img_url)
        db.session.add(image)
        db.session.flush()
        t = int(time.time())
        relation = Transfer(user_id=user_id, image_id=image.id, timestamp=str(t))
        db.session.add(relation)
        db.session.commit()
        return jsonify(url=img_url, code=200, msg='success with id')
    except Exception as e:
        return jsonify(url=img_url, code=500, msg='database error')


@transfer.route('/style_qlssh_is', methods=['POST'])
def style_qlssh_is():
    """
    青山绿水图保留原色
    @param image:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param alpha:参数
    @return code(200=正常返回，400=错误),url:图片地址
    """
    param = request.get_json()
    img_base64 = param.get('image')
    alpha = float(param.get('alpha'))
    user_id = param.get('id')
    if not all([img_base64, alpha]):
        return jsonify(code=400, msg='lack of parameters')

    img_path = utils.base64_to_imagefile(img_base64, save_path=INPUT_PATH)
    output_img_url = using_model(img_path, STYLE_QLSSH_PATH, alpha, True)
    img_url = HOST + '/' + str(output_img_url)
    if not user_id:
        return jsonify(url=img_url, code=200, msg='success without id')

    try:
        image = Image(url=img_url)
        db.session.add(image)
        db.session.flush()
        t = int(time.time())
        relation = Transfer(user_id=user_id, image_id=image.id, timestamp=str(t))
        db.session.add(relation)
        db.session.commit()
        return jsonify(url=img_url, code=200, msg='success with id')
    except Exception as e:
        return jsonify(url=img_url, code=500, msg='database error')


@transfer.route('/style_qjssh_no', methods=['POST'])
def style_qjssh_no():
    """
    浅绛山水画不保留原色
    @param image:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param alpha:参数
    @return code(200=正常返回，400=错误),url:图片地址
    """
    param = request.get_json()
    img_base64 = param.get('image')
    alpha = float(param.get('alpha'))
    user_id = param.get('id')
    if not all([img_base64, alpha]):
        return jsonify(code=400, msg='lack of parameters')

    img_path = utils.base64_to_imagefile(img_base64, save_path=INPUT_PATH)
    output_img_url = using_model(img_path, STYLE_QJSSH_PATH, alpha, False)
    img_url = HOST + '/' + str(output_img_url)
    if not user_id:
        return jsonify(url=img_url, code=200, msg='success without id')

    try:
        image = Image(url=img_url)
        db.session.add(image)
        db.session.flush()
        t = int(time.time())
        relation = Transfer(user_id=user_id, image_id=image.id, timestamp=str(t))
        db.session.add(relation)
        db.session.commit()
        return jsonify(url=img_url, code=200, msg='success with id')
    except Exception as e:
        return jsonify(url=img_url, code=500, msg='database error')


@transfer.route('/style_qjssh_is', methods=['POST'])
def style_qjssh_is():
    """
    浅绛山水画保留原色
    @param image:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param alpha:参数
    @return code(200=正常返回，400=错误),url:图片地址
    """
    param = request.get_json()
    img_base64 = param.get('image')
    alpha = float(param.get('alpha'))
    user_id = param.get('id')
    if not all([img_base64, alpha]):
        return jsonify(code=400, msg='lack of parameters')

    img_path = utils.base64_to_imagefile(img_base64, save_path=INPUT_PATH)
    output_img_url = using_model(img_path, STYLE_QJSSH_PATH, alpha, True)
    img_url = HOST + '/' + str(output_img_url)
    if not user_id:
        return jsonify(url=img_url, code=200, msg='success without id')

    try:
        image = Image(url=img_url)
        db.session.add(image)
        db.session.flush()
        t = int(time.time())
        relation = Transfer(user_id=user_id, image_id=image.id, timestamp=str(t))
        db.session.add(relation)
        db.session.commit()
        return jsonify(url=img_url, code=200, msg='success with id')
    except Exception as e:
        return jsonify(url=img_url, code=500, msg='database error')


@transfer.route('/style_any_no', methods=['POST'])
def style_any_no():
    """
    任意风格不保留原色
    @param image_style:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param image_content:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param alpha:参数
    @return code(200=正常返回，400=错误),url:图片地址
    """
    param = request.get_json()
    param = request.get_json()
    img_style_base64 = param.get('image_style')
    image_content_base64 = param.get('image_content')
    alpha = float(param.get('alpha'))
    user_id = param.get('id')
    if not all([img_style_base64, image_content_base64, alpha]):
        return jsonify(code=400, msg='lack of parameters')

    img_style_path = utils.base64_to_imagefile(img_style_base64, save_path=INPUT_PATH)
    time.sleep(1)
    image_content_path = utils.base64_to_imagefile(image_content_base64, save_path=INPUT_PATH)
    output_img_url = using_model(image_content_path, img_style_path, alpha, False)
    img_url = HOST + '/' + str(output_img_url)
    if not user_id:
        return jsonify(url=img_url, code=200, msg='success without id')

    try:
        image = Image(url=img_url)
        db.session.add(image)
        db.session.flush()
        t = int(time.time())
        relation = Transfer(user_id=user_id, image_id=image.id, timestamp=str(t))
        db.session.add(relation)
        db.session.commit()
        return jsonify(url=img_url, code=200, msg='success with id')
    except Exception as e:
        return jsonify(url=img_url, code=500, msg='database error')


@transfer.route('/style_any_is', methods=['POST'])
def style_any_is():
    """
    任意风格保留原色
    @param image_style:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param image_content:base64编码后的图片字符串，如data:image/jpg;base64,/9j/4AAQSkZJRgABAQ...
    @param alpha:参数
    @return code(200=正常返回，400=错误),url:图片地址
    """

    param = request.get_json()
    img_style_base64 = param.get('image_style')
    image_content_base64 = param.get('image_content')
    alpha = float(param.get('alpha'))
    user_id = param.get('id')
    if not all([img_style_base64, image_content_base64, alpha]):
        return jsonify(code=400, msg='lack of parameters')

    img_style_path = utils.base64_to_imagefile(img_style_base64, save_path=INPUT_PATH)
    time.sleep(1)
    image_content_path = utils.base64_to_imagefile(image_content_base64,save_path=INPUT_PATH)
    output_img_url = using_model(image_content_path, img_style_path, alpha, True)
    img_url = HOST + '/' + str(output_img_url)
    if not user_id:
        return jsonify(url=img_url, code=200, msg='success without id')

    try:
        image = Image(url=img_url)
        db.session.add(image)
        db.session.flush()
        t = int(time.time())
        relation = Transfer(user_id=user_id, image_id=image.id, timestamp=str(t))
        db.session.add(relation)
        db.session.commit()
        return jsonify(url=img_url, code=200, msg='success with id')
    except Exception as e:
        return jsonify(url=img_url, code=500, msg='database error')
