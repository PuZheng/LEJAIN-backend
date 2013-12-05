#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
本脚本用于创建测试数据，是为了帮助进行随意测试。本脚本基于数据库的初始化脚本
"""
from datetime import datetime
from setuptools import Command
from genuine_ap.models import (Tag, Product, Vendor)
from genuine_ap.utils import do_commit


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
        # products
        product1 = do_commit(Product(name=u'飞天茅台53度', code='854013',
                                     vendor=vendor1))
        product2 = do_commit(Product(name=u'红塔山(大经典)', code='987360',
                                     vendor=vendor2))
        # tags
        do_commit(Tag(token='1', product=product1,
                      manufacture_time=datetime.strptime('2010-11-11',
                                                         '%Y-%m-%d'),
                      expire_time=datetime.strptime('2020-11-11',
                                                    '%Y-%m-%d')))
        do_commit(Tag(token='2', product=product1,
                      manufacture_time=datetime.strptime('2011-12-12',
                                                         '%Y-%m-%d'),
                      expire_time=datetime.strptime('2021-12-12',
                                                    '%Y-%m-%d')))
        do_commit(Tag(token='3', product=product2,
                      manufacture_time=datetime.strptime('2010-11-11',
                                                         '%Y-%m-%d'),
                      expire_time=datetime.strptime('2011-11-11',
                                                    '%Y-%m-%d')))
        do_commit(Tag(token='4', product=product2,
                      manufacture_time=datetime.strptime('2011-12-12',
                                                         '%Y-%m-%d'),
                      expire_time=datetime.strptime('2012-12-12',
                                                    '%Y-%m-%d')))


if __name__ == "__main__":
    from distutils.dist import Distribution
    InitializeTestDB(Distribution()).run()
