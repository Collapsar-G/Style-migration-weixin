#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 19:40

'测试用文件'

__author__ = 'Judgement'

from flask import Blueprint

base = Blueprint('base', __name__)


@base.route('/')
def hello_world():
    return '陈阳真帅啊！！！我好爱！！！'
