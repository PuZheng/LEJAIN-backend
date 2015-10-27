#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from werkzeug.security import generate_password_hash

from lejian.tools.init_db import init_db
from lejian.tools.gen_roles import gen_roles
from lejian.tools.gen_vendors import gen_vendors
from lejian.tools.gen_spu_types import gen_spu_types
from lejian.models import User, SPU
from lejian.utils import do_commit


if __name__ == '__main__':
    init_db()
    roles = gen_roles()
    role_super_admin = [role for role in roles if role.name == '系统管理员'][0]

    print('create super admin ...')
    do_commit(User(role=role_super_admin, email='admin@lejian.com',
                   password=generate_password_hash('admin',
                                                   'pbkdf2:sha256')))

    vendor_motai, vendor_hongta = gen_vendors()
    spu_type_cigar, spu_type_spirit = gen_spu_types()

    spu1 = do_commit(SPU(name=u'飞天茅台53度', code='854013',
                         vendor=vendor_motai, msrp=1300,
                         spu_type=spu_type_spirit,
                         rating=4.0))
    # spu2 = do_commit(SPU(name=u'红塔山(大经典)', code='987360',
    #                      vendor=vendor_hongta, msrp=50, spu_type=spu_type_cigar,
    #                      rating=4.0))
    do_commit(SPU(name=u'茅台迎宾酒', code='582677',
                  vendor=vendor_motai, msrp=100, spu_type=spu_type_spirit,
                  rating=3.0))
