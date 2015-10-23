#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from werkzeug.security import generate_password_hash

from lejian.tools.init_db import init_db
from lejian.tools.gen_roles import gen_roles
from lejian.tools.gen_vendors import gen_vendors
from lejian.tools.gen_spu_types import gen_spu_types
from lejian.models import User
from lejian.utils import do_commit


if __name__ == '__main__':
    init_db()
    roles = gen_roles()
    role_super_admin = [role for role in roles if role.name == '系统管理员'][0]

    print('create super admin ...')
    do_commit(User(role=role_super_admin, email='admin@lejian.com',
                   password=generate_password_hash('admin',
                                                   'pbkdf2:sha256')))

    vendors = gen_vendors()
    spu_types = gen_spu_types()
