#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 19:32

'项目入口'

__author__ = 'Judgement'

from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app('dev')

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)
"""
cmd
python manage.py db init 初始化数据库
python manage.py db migrate -m "message" 提交变更
python manage.py db upgrade 升级变更
python manage.py db downgrade 降级
 
python manage.py runserver --host 127.0.0.1 --port 3268  运行服务器
"""

if __name__ == '__main__':
    manager.run()
