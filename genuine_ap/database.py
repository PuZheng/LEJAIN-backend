# -*- coding: utf-8 -*-
from genuine_ap.basemain import app
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
import sqlalchemy as sa
from sqlalchemy_utils import coercion_listener
sa.event.listen(sa.orm.mapper, 'mapper_configured', coercion_listener)


def init_db():
    # 必须要import models, 否则不会建立表
    import genuine_ap.models
    db.create_all()
