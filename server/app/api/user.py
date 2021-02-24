#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 22:19

'和用户相关的接口'

__author__ = 'Judgement'

from flask import Blueprint, request, jsonify, session
import time
import datetime
from app.database.models import db, Transfer, Image
from app.database.models import User
import requests

user = Blueprint('user', __name__)

appid = "wx7330267cab93fa97"
secret = "d2d27f80db202377fbb8ca9d49eab458"


@user.route('/login', methods=['POST'])
def login():
    """
    @param:     code
    @return:    code(200 正常，400 输入异常, 500 服务器异常)
                msg(信息)
    """
    param = request.get_json()
    # id = param.get('id')
    # name = param.get('name')
    code = param.get('code')
    # if not all([id, name]):
    #     return jsonify(code=400, msg='lack of parameters')
    if not all([code]):
        return jsonify(code=400, msg='lack of parameters')
    # 先检测用户是否已在数据库

    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'.format(
        appid=appid, secret=secret, code=code)
    res = requests.get(url)
    openid = res.json().get('openid')
    session_key = res.json().get('session_key')
    # except:
    #     return jsonify(code=400, msg='获取openid错误')
    id = openid
    user = User.query.filter_by(id=id).first()
    if not user:
        # 不在数据库，入库
        user = User(id=id)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return jsonify(code=500, msg='database error')

    session['id'] = user.id
    return jsonify(code=200, msg='success', id=id)


# @user.route('/check', methods=['GET'])
# def check():
#     id = session.get('id')
#     return id


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
    返回一个用户十天内的历史记录
    @return:    code(200,400,500)
                msg
                data:[image](images)
                    image=  {
                                url
                                timestamp
                            }
    """
    # param = request.get_json()
    user_id = session['id']
    # user_id = param.get('id')
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

    today = datetime.date.today()
    day_10 = today - datetime.timedelta(days=10)
    day_10_start_time = int(time.mktime(time.strptime(str(day_10), '%Y-%m-%d')))
    images = []
    for item in tables:
        if item.timestamp >= str(day_10_start_time):
            image = {}
            image['url'] = item.url
            image['timestamp'] = item.timestamp
            images.append(image)
    return jsonify(code=200, msg='success', data=images)


@user.route('/total', methods=['GET'])
def total():
    """
        返回一个用户的累积使用次数
        @return:    code(200,400,500)
                    msg
                    count
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
            .count()
    except Exception as e:
        return jsonify(code=500, msg='database error')
    return jsonify(code=200, msg='success', count=tables)
