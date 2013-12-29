# -*- coding: UTF-8 -*-

import pyfeature

from pyfeature import (Feature, Scenario, given, and_, when, then,
                       flask_sqlalchemy_setup)
from genuine_ap.basemain import app
from genuine_ap.database import db


def test():
    flask_sqlalchemy_setup(app, db)
    with Feature('test spu', step_files=['genuine_ap.tests.steps.spu']):
        with Scenario('create spu'):
            spu = given('create a spu with pictures',
                        pic_file_list=['data/1.jpg', 'data/2.jpg'])
            then('spu will have a logo created by first picture', spu=spu,
                 pic_file=['data/1.jpg'])
            then('spu have the correct pictures', spu=spu,
                 pic_file_list=['data/1.jpg', 'data/2.jpg'])

        with Scenario('create spu'):
            given('change the pictures of spu',
                  spu=spu, pic_file_list=['data/2.jpg', 'data/3.jpg'])
            then('spu will have a logo created by first picture', spu=spu,
                 pic_file=['data/2.jpg'])
            then('spu have the correct pictures', spu=spu,
                 pic_file_list=['data/1.jpg', 'data/2.jpg'])

if __name__ == '__main__':
    test()
