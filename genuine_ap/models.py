# -*- coding: UTF-8 -*-

from datetime import datetime
from genuine_ap.database import db


class Tag(db.Model):

    __tablename__ = 'TB_TAG'

    token = db.Column(db.String(32), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('TB_PRODUCT.name'),
                           nullable=False)
    product = db.relationship('Product')
    create_time = db.Column(db.DateTime, default=datetime.now)
    manufacture_time = db.Column(db.DateTime)
    expire_time = db.Column(db.DateTime)


class Product(db.Model):

    __tablename__ = 'TB_PRODUCT'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    code = db.Column(db.String(32), unique=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('TB_VENDOR.name'),
                          nullable=False)
    vendor = db.relationship('Vendor', backref="product_list")


class Vendor(db.Model):

    __tablename__ = 'TB_VENDOR'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
