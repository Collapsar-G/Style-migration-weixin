#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 22:19

'和用户相关的接口'

__author__ = 'Judgement'

from flask import Blueprint, request, jsonify, session

from app.database.models import db, Transfer, Image
from app.database.models import User

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login():
    """
    @param:     id(用户的唯一标识)
    @param:     name(用户名)
    @return:    code(200 正常，400 输入异常, 500 服务器异常)
                msg(信息)
    """
    param = request.get_json()
    id = param.get('id')
    name = param.get('name')
    if not all([id, name]):
        return jsonify(code=400, msg='lack of parameters')

    # 先检测用户是否已在数据库
    user = User.query.filter_by(id=id).first()
    if not user:
        # 不在数据库，入库
        user = User(id=id, name=name)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return jsonify(code=500, msg='database error')

    session['id'] = user.id
    return jsonify(code=200, msg='success')


@user.route('/check', methods=['GET'])
def check():
    id = session.get('id')
    return id


@user.route('/logout', methods=['GET'])
def logout():
    """
    退出登录，释放资源
    @return:    code(200 正常)
                msg(信息)
    """
    session.clear()
    return jsonify(code=200, msg='quit')


@user.route('/upload', methods=['POST'])
def upload():
    pass


@user.route('/history', methods=['GET'])
def history():
    """
    返回一个用户的历史记录
    @return:    code(200,400,500)
                msg
                data:[image](images)
                    image=  {
                                url
                                timestamp
                            }
    """
    user_id = session['id']
    if not user_id:
        return jsonify(code=400, msg='user illegal')

    try:
        tables = Transfer.query \
            .filter_by(user_id=user_id) \
            .join(Image, Transfer.image_id == Image.id) \
            .with_entities(Transfer.user_id, Transfer.image_id, Transfer.timestamp, Image.url) \
            .order_by(Transfer.timestamp.desc()) \
            .all()
    except Exception as e:
        return jsonify(code=500, msg='database error')

    images = []
    for item in tables:
        image = {}
        image['url'] = item.url
        image['timestamp'] = item.timestamp
        images.append(image)
    return jsonify(code=200, msg='success', data=images)

