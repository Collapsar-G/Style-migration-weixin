#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/7 18:27

'表的基本对象结构'

__author__ = 'Judgement'

from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(256), nullable=False)


class Transfer(db.Model):
    __tablename__ = 'transfer'
    user_id = db.Column(db.String(64), primary_key=True)
    image_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(64), primary_key=True)
