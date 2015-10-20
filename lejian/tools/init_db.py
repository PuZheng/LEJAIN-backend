#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from lejian.basemain import app
from lejian.database import db


def init_db():
    print("初始化开始, 数据库是: " + app.config["SQLALCHEMY_DATABASE_URI"])
    db.drop_all()
    __import__('lejian.models')
    db.create_all()

if __name__ == "__main__":
    init_db()
