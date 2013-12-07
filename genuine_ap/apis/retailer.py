# -*- coding: UTF-8 -*-
from genuine_ap import models


def find_nearby_retailers(longitude, lattitude):
    #TODO a dumb implementation
    cnt = models.Retailer.query.count()
    return models.Retailer.query.all(), (100, ) * cnt
