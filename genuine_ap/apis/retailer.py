# -*- coding: UTF-8 -*-
import random
from flask import url_for

from genuine_ap import models
from genuine_ap.apis import wraps, ModelWrapper


def find_retailers(longitude, latitude, spu_id=None, max_distance=1500):
    #TODO a dumb implementation
    cnt = models.Retailer.query.count()
    retailers = models.Retailer.query.all()
    distance_list = []
    for retailer in retailers:
        offset = random.randrange(-10, stop=10) * 0.0001
        retailer.longitude = longitude + offset
        retailer.latitude = latitude + offset
        distance_list.append(abs(offset * 110000))
    if spu_id:
        retailers = [retailer for retailer in retailers if
                     spu_id in [spu.id for spu in retailer.spu_list]]
    return wraps(retailers), distance_list


class RetailerWrapper(ModelWrapper):

    def as_dict(self):

        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'rating': self.desc,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'logo': self.logo,
        }

    @property
    def logo(self):
        retailer_dir = 'retailer_pics/%s/' % self.id
        return url_for('static', filename=retailer_dir + 'logo.jgp')
