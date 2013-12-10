# -*- coding: UTF-8 -*-
from flask import url_for

from genuine_ap import models
from genuine_ap.apis import wraps, ModelWrapper


def find_retailers(longitude, lattitude, spu_id=None, max_distance=1500):
    #TODO a dumb implementation
    cnt = models.Retailer.query.count()
    retailers = models.Retailer.query.all()
    if spu_id:
        retailers = [retailer for retailer in retailers if
                     spu_id in [spu.id for spu in retailers.spu_list]]
    return wraps(retailers), (100, ) * cnt


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
