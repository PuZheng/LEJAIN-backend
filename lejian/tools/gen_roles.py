#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from werkzeug.security import generate_password_hash

import lejian.const as const
from lejian.models import Role, User
from lejian.utils import do_commit


def gen_roles():
    print('创建用户角色...')
    do_commit(Role(name=u'普通用户'))
    do_commit(Role(name=u'厂商'))
    do_commit(Role(name=u'零售商'))
    role_super_admin = do_commit(Role(id=const.SUPER_ADMIN,
                                      name='系统管理员'))
    # super admin
    print(generate_password_hash('admin', 'pbkdf2:sha256'))
    do_commit(User(role=role_super_admin, email='admin@lejian.com',
                   password=generate_password_hash('admin', 'pbkdf2:sha256')))


if __name__ == '__main__':
    gen_roles()
