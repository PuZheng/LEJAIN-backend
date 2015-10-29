# -*- coding: UTF-8 -*-
import sys
import os
import re
import shutil
from flask import url_for, current_app
from datetime import datetime

# from sqlalchemy_utils import types as sa_utils_types
# from flask.ext.babel import _
from .database import db
import os.path
from path import path
from lejian.utils import to_camel_case

retailer_and_spu = db.Table('TB_RETAILER_AND_SPU',
                            db.Column('retailer_id', db.Integer,
                                      db.ForeignKey(
                                          'TB_RETAILER.id')),
                            db.Column('spu_id', db.Integer,
                                      db.ForeignKey('TB_SPU.id')))


class Unicodable(object):

    @property
    def _unicode_fields(self):
        return [k for k in self.__mapper__.columns.keys() if k != 'id']

    def __unicode__(self):
        ret = self.__class__.__name__
        if self.id:
            ret += ' ' + str(self.id) + ' '
        l = []
        for field in self._unicode_fields:
            value = getattr(self, field)
            if value:
                l.append([field, value])

        return (u'<' + ret + u'(' + ','.join([':'.join(map(unicode, [k, v]))
                                              for k, v in l]) + ')' + '>')

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class JSONSerializable(object):

    def __json__(self, camel_case=True, excluded=set()):
        ret = {}
        for c in self.__mapper__.columns:
            if c.name not in excluded:
                v = getattr(self, c.name)
                if isinstance(v, datetime):
                    v = v.strftime('%Y-%m-%d %H:%M:%S')
                ret[c.name] = v
        return to_camel_case(ret) if camel_case else ret


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
    spu = db.relationship('SPU', backref='sku_list')
    manufacture_date = db.Column(db.Date)
    expire_date = db.Column(db.Date)
    token = db.Column(db.String(32), unique=True, nullable=False)
    checksum = db.Column(db.String(32), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    verify_count = db.Column(db.Integer, nullable=False, default=0)
    last_verify_time = db.Column(db.DateTime, default=datetime.now)

    def __unicode__(self):
        return self.token


class SPU(db.Model, JSONSerializable, Unicodable):

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
    create_time = db.Column(db.DateTime, default=datetime.now)
    enabled = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(256))

    @property
    def pics(self):
        ret = []
        dir_ = path.joinpath(current_app.config['ASSETS_DIR'], 'spu_pics',
                             str(self.id))
        for fname in dir_.files():
            if path.basename(fname) != 'icon.jpg' and \
                    re.match(r'.+\.(jpeg|jpg)', fname, re.IGNORECASE):
                ret.append(fname)
        return ret

    @property
    def icon(self):
        dir_ = path.joinpath(current_app.config['ASSETS_DIR'], 'spu_pics',
                             str(self.id))
        ret = dir_.glob('icon.jpg')
        return ret and ret[0]

    @property
    def pic_url_list(self):
        ret = []
        spu_dir = os.path.join('spu_pics', str(self.vendor_id), str(self.id))
        if os.path.exists(os.path.join('static', spu_dir)):
            for fname in path(os.path.join('static', spu_dir)).files():
                fname = os.path.basename(fname)
                if fname != 'icon.jpg' and re.match(r'.+\.(jpeg|jpg)', fname,
                                                    re.IGNORECASE):
                    filename = os.path.join(spu_dir, os.path.basename(fname))
                    if sys.platform.startswith("win32"):
                        filename = filename.replace(os.path.sep, os.path.altsep)
                    ret.append(url_for('static', filename=filename))
        return sorted(ret)

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
        spu_dir = os.path.join('static', 'spu_pics',
                               str(self.vendor.id), str(self.id))
        from .utils import assert_dir
        assert_dir(spu_dir)
        to_be_removed = []
        haystack = [os.path.basename(fname) for fname in value]
        haystack.append('icon.jpg')
        for fname in path(spu_dir).files():
            if os.path.basename(fname) not in haystack:
                to_be_removed.append(fname)
        from .utils import resize_and_crop
        resize_and_crop(value[0], os.path.join(spu_dir, 'icon.jpg'),
                        (96, 96), 'middle')
        for fname in value:
            shutil.copy(fname, spu_dir)
            os.remove(fname)
        for fname in to_be_removed:
            os.unlink(fname)

    def __json__(self, camel_case=True, excluded=set()):
        ret = super(SPU, self).__json__(camel_case, excluded)
        ret['spuType' if camel_case else 'spu_type'] = self.spu_type.__json__()
        ret['pics'] = self.pics
        ret['icon'] = self.icon
        return ret


class Vendor(db.Model):

    __tablename__ = 'TB_VENDOR'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    brief = db.Column(db.String(256))
    create_time = db.Column(db.DateTime, default=datetime.now)
    telephone = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(256))
    email = db.Column(db.String(32), nullable=False,
                      doc=u'客服邮箱')
    website = db.Column(db.String(32), nullable=False)
    weibo = db.Column(db.String(32), doc=u'微博UID')
    weibo_link = db.Column(db.String(32), doc=u"微博主页")
    weixin_follow_link = db.Column(db.String(32),
                                   doc=u'微信加关注链接')
    weixin_number = db.Column(db.String(32), doc=u'微信号')
    administrator_id = db.Column(db.Integer, db.ForeignKey('TB_USER.id'),
                                 nullable=False)
    administrator = db.relationship('User',
                                    backref=db.backref("vendor",
                                                       uselist=False))
    enabled = db.Column(db.Boolean, default=False)

    def __unicode__(self):
        return self.name


class Comment(db.Model):

    __tablename__ = 'TB_COMMENT'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    spu_id = db.Column(db.Integer, db.ForeignKey('TB_SPU.id'),
                       nullable=False)
    spu = db.relationship('SPU', backref='comment_list')
    user_id = db.Column(db.Integer, db.ForeignKey('TB_USER.id'),
                        nullable=False)
    user = db.relationship('User')
    rating = db.Column(db.Float, nullable=False)


class User(db.Model, JSONSerializable, Unicodable):

    __tablename__ = 'TB_USER'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(128), doc=u'保存为明文密码的sha256值')
    role_id = db.Column(db.Integer, db.ForeignKey('TB_ROLE.id'),
                        nullable=False)
    role = db.relationship('Role')
    created_at = db.Column(db.DateTime, default=datetime.now)
    enabled = db.Column(db.Boolean, default=False)

    def __json__(self, camel_case=True, excluded=set()):
        ret = super(User, self).__json__(camel_case, excluded)
        if 'role' not in excluded:
            ret['role'] = self.role.__json__()
        return ret


class Customer(db.Model):

    __tablename__ = 'TB_CUSTOMER'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(128), doc=u'保存为明文密码的sha256值')
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __unicode__(self):
        return self.name


class Role(db.Model, JSONSerializable, Unicodable):

    __tablename__ = 'TB_ROLE'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)


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
    administrator_id = db.Column(db.Integer, db.ForeignKey('TB_USER.id'),
                                 nullable=False)
    administrator = db.relationship('User',
                                    backref=db.backref("retailer",
                                                       uselist=False))
    enabled = db.Column(db.Boolean, default=False)

    def __unicode__(self):
        return self.name

    @property
    def icon(self):
        if os.path.exists(os.path.join('static', 'retailer_pics',
                                       str(self.id) + '_icon.jpg')):
            return url_for('static',
                           filename='retailer_pics/' + str(self.id) +
                           '_icon.jpg')
        return ''

    @icon.setter
    def icon(self, value):
        if value:
            if not self.id:
                # when create
                self.temp_icon = value


class Favor(db.Model):

    __tablename__ = 'TB_FAVOR'

    id = db.Column(db.Integer, primary_key=True)
    spu_id = db.Column(db.Integer, db.ForeignKey('TB_SPU.id'),
                       nullable=False)
    spu = db.relationship('SPU', backref='favor_list')
    user_id = db.Column(db.Integer, db.ForeignKey('TB_USER.id'),
                        nullable=False)
    user = db.relationship('User', backref='favor_list')
    create_time = db.Column(db.DateTime, default=datetime.now)


class SPUType(db.Model, JSONSerializable, Unicodable):

    __tablename__ = 'TB_SPU_TYPE'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    weight = db.Column(db.Integer, doc=u'SPU分类的权重，越高代表越优先显示',
                       default=0)
    pic_path = db.Column(db.String(256), nullable=False)
    enabled = db.Column(db.Boolean, default=False)

    def __json__(self, camel_case=True, excluded=set()):

        ret = super(SPUType, self).__json__(camel_case, excluded)
        ret['spuCnt' if camel_case else 'spu_cnt'] = len(self.spu_list)
        return ret


class Config(db.Model):

    __tablename__ = 'TB_CONFIG'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    brief = db.Column(db.String(128))
    type_ = db.Column(db.String(64))
    value = db.Column(db.String(128))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<Config: %s>" % self.name.encode("utf-8")
