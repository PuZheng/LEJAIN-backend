#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from lejian.tools.init_db import init_db
from lejian.tools.gen_roles import gen_roles

if __name__ == '__main__':
    init_db()
    gen_roles()
