#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
本脚本用于创建测试数据，是为了帮助进行随意测试。本脚本基于数据库的初始化脚本
"""
from datetime import datetime
from setuptools import Command

from werkzeug.security import generate_password_hash

__import__('genuine_ap.basemain')
from genuine_ap.models import (Tag, SPU, SKU, Vendor, Group, User, Comment,
                               Favor, Retailer, SPUType)
from genuine_ap.utils import do_commit
from genuine_ap import const


class InitializeTestDB(Command):
    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        from genuine_ap.tools import build_db
        build_db.build_db()
        # vendors
        vendor1 = do_commit(Vendor(name=u'贵州茅台酒厂有限公司'))
        vendor2 = do_commit(Vendor(name=u'红塔山集团'))
        # spu types
        spu_type1 = do_commit(SPUType(name=u'香烟'))
        spu_type2 = do_commit(SPUType(name=u'国产白酒', weight=1))
        # spus
        spu1 = do_commit(SPU(name=u'飞天茅台53度', code='854013',
                             vendor=vendor1, msrp=1300, spu_type=spu_type2,
                             rating=4.0))
        spu2 = do_commit(SPU(name=u'红塔山(大经典)', code='987360',
                             vendor=vendor2, msrp=50, spu_type=spu_type1,
                             rating=4.0))
        do_commit(SPU(name=u'茅台迎宾酒', code='582677',
                      vendor=vendor1, msrp=100, spu_type=spu_type2,
                      rating=3.0))
        # skus
        sku1 = do_commit(SKU(spu=spu1,
                             manufacture_time=datetime.strptime('2010-11-11',
                                                                '%Y-%m-%d'),
                             expire_time=datetime.strptime('2020-11-11',
                                                           '%Y-%m-%d')))
        sku2 = do_commit(SKU(spu=spu1,
                             manufacture_time=datetime.strptime('2011-12-12',
                                                                '%Y-%m-%d'),
                             expire_time=datetime.strptime('2021-12-12',
                                                           '%Y-%m-%d')))
        sku3 = do_commit(SKU(spu=spu2,
                             manufacture_time=datetime.strptime('2010-11-11',
                                                                '%Y-%m-%d'),
                             expire_time=datetime.strptime('2011-11-11',
                                                           '%Y-%m-%d')))
        sku4 = do_commit(SKU(spu=spu2,
                             manufacture_time=datetime.strptime('2011-12-12',
                                                                '%Y-%m-%d'),
                             expire_time=datetime.strptime('2012-12-12',
                                                           '%Y-%m-%d')))
        # tags
        do_commit(Tag(token="000001", sku=sku1))
        do_commit(Tag(token="000002", sku=sku2))
        do_commit(Tag(token="000003", sku=sku3))
        do_commit(Tag(token="000004", sku=sku4))
        # groups
        group1 = do_commit(Group(id=const.CUSTOMER_GROUP, name=u'普通客户'))
        do_commit(Group(id=const.VENDOR_GROUP, name=u'生产厂家'))
        do_commit(Group(id=const.RETAILER_GROUP, name=u'零售商'))
        # users
        user1 = do_commit(User(group=group1, name=u'liubei',
                               password=generate_password_hash(
                                   'liubei', 'pbkdf2:sha256')))
        user2 = do_commit(User(group=group1, name=u'guanyu',
                               password=generate_password_hash(
                                   'guanyu', 'pbkdf2:sha256')))
        user3 = do_commit(User(group=group1, name=u'zhangfei',
                               password=generate_password_hash(
                                   'guanyu', 'pbkdf2:sha256')))
        # comments
        do_commit(Comment(content=u'好酒!', spu=spu1, user=user1, rating=4.0))
        do_commit(Comment(content=u'好酒!!', spu=spu1, user=user2, rating=4.5))
        do_commit(Comment(content=u'好酒!!!', spu=spu1, user=user3, rating=5.0))
        do_commit(Comment(content=u'烂烟~', spu=spu2, user=user1, rating=3.0))
        do_commit(Comment(content=u'烂烟~~', spu=spu2, user=user2, rating=2.5))
        do_commit(Comment(content=u'烂烟~~~', spu=spu2, user=user3, rating=2.0))
        # favors
        do_commit(Favor(spu=spu1, user=user1))
        do_commit(Favor(spu=spu1, user=user2))
        do_commit(Favor(spu=spu1, user=user3))
        do_commit(Favor(spu=spu2, user=user1))
        # retailers
        do_commit(Retailer(name=u'A烟酒专卖', rating=4.0, longitude=1.0,
                           latitude=1.0, address=u'杭州市西湖区申花路789号',
                           spu_list=[spu1, spu2]))
        do_commit(Retailer(name=u'B烟酒专卖', rating=4.5, longitude=1.0,
                           latitude=1.0, address=u'杭州市西湖区古墩路83号',
                           spu_list=[spu2]))


if __name__ == "__main__":
    from distutils.dist import Distribution
    InitializeTestDB(Distribution()).run()
