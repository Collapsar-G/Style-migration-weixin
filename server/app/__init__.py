#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 19:55

'app实例'

__author__ = 'Judgement'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config_map

db = SQLAlchemy()


def create_app(name):
    """
    创建app实例
    @param name:配置环境的名称，可选 dev， pro
    @return: app实例
    """
    app = Flask(__name__, static_folder='../static')

    # 配置
    app.config.from_object(config_map[name])

    # 数据库
    db.init_app(app)

    # 接口

    from algorithm.style_api import style
    from app.api.transfer import transfer
    from app.api.base import base
    from app.api.user import user
    from app.api.feedback import feedback
    app.register_blueprint(style)
    app.register_blueprint(base)
    app.register_blueprint(transfer, url_prefix='/transfer')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(feedback, url_prefix='/feedback')


    return app
