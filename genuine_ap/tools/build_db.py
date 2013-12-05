# -*- coding: utf-8 -*-
import sys
from getopt import getopt
from genuine_ap.basemain import app


def build_db():
    msg = u"初始化开始, 数据库是: " + app.config["SQLALCHEMY_DATABASE_URI"]
    app.logger.info(msg)
    import os
    dbstr = app.config["SQLALCHEMY_DATABASE_URI"]
    if dbstr.startswith("sqlite"):
        dir = os.path.split(dbstr[10:])[0]
        if dir and not os.path.exists(dir):
            os.makedirs(dir)
    from genuine_ap.database import db, init_db
    db.drop_all()
    init_db()
    msg = u"初始化完成"
    app.logger.info(msg)

if __name__ == "__main__":
    opts, _ = getopt(sys.argv[1:], "s:h")
    for o, v in opts:
        if o == "-h":
            print __doc__
            exit(1)
        else:
            print "unknown option: " + o
    build_db()
