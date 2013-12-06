# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-

from genuine_ap.utils import find_model


def find_nearby_retailers(longitude, lattitude):
    #TODO a dumb implementation
    cnt = find_model('TB_RETAILER').query.count()
    return find_model('TB_RETAILER').query.all(), (100, ) * cnt
