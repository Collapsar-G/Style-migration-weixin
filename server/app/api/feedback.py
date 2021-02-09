#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/9 13:44

"""意见反馈接口"""

__author__ = 'Collapsar-G'

import traceback
import requests
from flask import Blueprint, request, jsonify, url_for, session
import json

feedback = Blueprint('feedback', __name__)


@feedback.route('/test')
def testfeedback():
    return "feedback测试成功"


@feedback.route('/feedback_content', methods=['POST'])
def feedback_content():
    """
        意见反馈s
        @param content:用户反馈的内容
        @return code(200=正常返回，400=错误),url:图片地址
        """
    param = request.get_json()
    content = param.get('content')
    if not all([content]):
        return jsonify(code=400, msg='lack of parameters')
    try:
        key = "这是一个秘密"  # your-key
        url = "https://sctapi.ftqq.com/" + key + '.send'
        payload = {'title': '国风小程序意见反馈', 'desp': content}
        requests.post(url, params=payload)
    except:
        return jsonify(code=400, msg='server服务错误')

    return jsonify(code=200, msg='success')
