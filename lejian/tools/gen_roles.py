#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from lejian.models import Role
from lejian.utils import do_commit


def gen_roles():
    print('创建用户角色...')
    return [
        do_commit(Role(name='普通用户')),
        do_commit(Role(name='厂商')),
        do_commit(Role(name='零售商')),
        do_commit(Role(name='系统管理员'))
    ]


if __name__ == '__main__':
    gen_roles()
