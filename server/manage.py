#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 19:32

'项目入口'

__author__ = 'Judgement'

from app import create_app

app = create_app('dev')

if __name__ == '__main__':
    app.run()
