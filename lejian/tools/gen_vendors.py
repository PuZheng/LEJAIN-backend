# -*- coding: UTF-8 -*-
from werkzeug.security import generate_password_hash

from lejian.utils import do_commit
from lejian.models import Vendor, User, Role


def gen_vendors():
    print('create vendors...')
    vendor_role = Role.query.filter(Role.name == '厂商').one()
    motai_admin = do_commit(User(role=vendor_role, name=u'maotai',
                                 password=generate_password_hash(
                                     'maotai', 'pbkdf2:sha256')))
    hongta_admin = do_commit(User(role=vendor_role, name=u'hongta',
                                  password=generate_password_hash(
                                      'hongta', 'pbkdf2:sha256')))
    # vendors
    brief = ('贵州茅台酒股份有限公司是由中国贵州茅台酒厂有限责任公司、贵州茅台'
             '酒厂技术开发公司、贵州省轻纺集体工业联社、深圳清华大学研究院、中'
             '国食品发酵工业研究所、北京糖业烟酒公司、江苏省糖烟酒总公司、上海'
             '捷强烟草糖酒（集团）有限公司等八家公司共同发起，并经过贵州省人民'
             '政府黔府函字（1999）291号文件批准设立的股份有限公司，注册资本为'
             '一亿八千五百万元')
    vendor1 = do_commit(Vendor(name=u'贵州茅台酒厂有限公司',
                               telephone="0571-00000000",
                               address=u'贵州芜湖市天堂区1122路',
                               email='support@motai.com',
                               website='http://www.motail.com',
                               brief=brief, administrator=motai_admin))
    brief = ('红塔烟草（集团）有限责任公司，创业于1956年，从一个小规模的烟叶复'
             '烤厂到名列中国第一，世界前列的现代化跨国烟草企业集团，红塔集团的'
             '发展史，就是一部中国民族工业不断求新图变追赶世界先进水平的演进史')
    vendor2 = do_commit(Vendor(name=u'红塔山集团',
                               telephone="0571-11111111",
                               email='support@hongta.com',
                               address=u'贵州芜湖市天堂区1122路',
                               website='http://hongta.com',
                               brief=brief[:256],
                               administrator=hongta_admin))
    return [vendor1, vendor2]
