# -*- coding: UTF-8 -*-
import os
import re
import shutil
from flask import url_for
from datetime import datetime

from .database import db
import posixpath
from path import path

retailer_and_spu = db.Table('TB_RETAILER_AND_SPU',
                            db.Column('retailer_id', db.Integer,
                                      db.ForeignKey(
                                          'TB_RETAILER.id')),
                            db.Column('spu_id', db.Integer,
                                      db.ForeignKey('TB_SPU.id')))


class Tag(db.Model):

    __tablename__ = 'TB_TAG'

    token = db.Column(db.String(32), primary_key=True)
    sku_id = db.Column(db.Integer, db.ForeignKey('TB_SKU.id'),
                       nullable=False)
    sku = db.relationship('SKU')
    create_time = db.Column(db.DateTime, default=datetime.now)


class SKU(db.Model):

    __tablename__ = 'TB_SKU'

    id = db.Column(db.Integer, primary_key=True)
    spu_id = db.Column(db.Integer, db.ForeignKey('TB_SPU.id'),
                       nullable=False)
    spu = db.relationship('SPU')
    manufacture_date = db.Column(db.Date)
    expire_date = db.Column(db.Date)
    token = db.Column(db.String(32), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __unicode__(self):
        return self.spu.name + '(%s)' % self.token


class SPU(db.Model):

    __tablename__ = 'TB_SPU'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    code = db.Column(db.String(32), unique=True, nullable=False)
    msrp = db.Column(db.Float, doc=u'建议零售价，单位为元')
    vendor_id = db.Column(db.Integer, db.ForeignKey('TB_VENDOR.id'),
                          nullable=False)
    vendor = db.relationship('Vendor', backref="spu_list")
    spu_type_id = db.Column(db.Integer, db.ForeignKey('TB_SPU_TYPE.id'),
                            nullable=False)
    spu_type = db.relationship('SPUType', backref="spu_list")
    rating = db.Column(db.Float, nullable=False)

    @property
    def pic_url_list(self):
        ret = []
        spu_dir = posixpath.join('spu_pics', str(self.vendor_id), str(self.id))
        if posixpath.exists(posixpath.join('static', spu_dir)):
            for fname in path(posixpath.join('static',
                                             spu_dir)).files():
                fname = path.basename(fname)
                if fname != 'icon.jpg' and re.match(r'.+\.(jpeg|jpg)', fname,
                                                    re.IGNORECASE):
                    filename = posixpath.join(spu_dir, path.basename(fname))
                    ret.append(url_for('static', filename=filename))
        return ret

    @pic_url_list.setter
    def pic_url_list(self, value):
        if value:
            if not self.vendor.id or not self.id:
                # when create
                self.temp_pic_url_list = value
            else:
                self.save_pic_url_list(value)

    def save_pic_url_list(self, value):
        assert self.vendor.id and self.id
        spu_dir = posixpath.join('static', 'spu_pics',
                                 str(self.vendor.id), str(self.id))
        from .utils import assert_dir
        assert_dir(spu_dir)
        from .utils import resize_and_crop
        resize_and_crop(value[0], posixpath.join(spu_dir, 'icon.jpg'),
                        (96, 96), 'middle')
        for fname in value:
            shutil.copy(fname, spu_dir)
            os.remove(fname)

    def __unicode__(self):
        return self.name + u'(%s)' % self.code


class Vendor(db.Model):

    __tablename__ = 'TB_VENDOR'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    brief = db.Column(db.String(256))
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __unicode__(self):
        return self.name


class Comment(db.Model):

    __tablename__ = 'TB_COMMENT'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    spu_id = db.Column(db.Integer, db.ForeignKey('TB_SPU.id'),
                       nullable=False)
    spu = db.relationship('SPU')
    user_id = db.Column(db.Integer, db.ForeignKey('TB_USER.id'),
                        nullable=False)
    user = db.relationship('User')
    rating = db.Column(db.Float, nullable=False)


class User(db.Model):

    __tablename__ = 'TB_USER'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(128), doc=u'保存为明文密码的md5值')
    group_id = db.Column(db.Integer, db.ForeignKey('TB_GROUP.id'),
                         nullable=False)
    group = db.relationship('Group')
    create_time = db.Column(db.DateTime, default=datetime.now)


class Group(db.Model):

    __tablename__ = 'TB_GROUP'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    default_url = db.Column(db.String(256), nullable=False)


class Retailer(db.Model):

    __tablename__ = 'TB_RETAILER'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    brief = db.Column(db.String(256))
    rating = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    spu_list = db.relationship('SPU', secondary=retailer_and_spu,
                               backref='retailer_list')
    address = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


    def __unicode__(self):
        return self.name

class Favor(db.Model):

    __tablename__ = 'TB_FAVOR'

    id = db.Column(db.Integer, primary_key=True)
    spu_id = db.Column(db.Integer, db.ForeignKey('TB_SPU.id'),
                       nullable=False)
    spu = db.relationship('SPU')
    user_id = db.Column(db.Integer, db.ForeignKey('TB_USER.id'),
                        nullable=False)
    user = db.relationship('User')
    create_time = db.Column(db.DateTime, default=datetime.now)


class SPUType(db.Model):

    __tablename__ = 'TB_SPU_TYPE'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    weight = db.Column(db.Integer, doc=u'SPU分类的权重，越高代表越优先显示',
                       default=0)
    pic_path = db.Column(db.String(256), nullable=False)

    def __unicode__(self):
        return self.name
