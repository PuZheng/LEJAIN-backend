#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from lejian.models import SPUType
from lejian.utils import do_commit


def gen_spu_types():
    print('create spu types...')
    return [
        do_commit(SPUType(name='香烟', enabled=True, weight=2,
                          pic_path='static/spu_type_pics/1.jpg')),
        do_commit(SPUType(name=u'国产白酒', weight=1,
                          pic_path='static/spu_type_pics/2.jpg'))
    ]


if __name__ == '__main__':
    gen_spu_types()
