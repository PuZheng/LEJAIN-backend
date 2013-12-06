# -*- coding: UTF-8 -*-
import os

from flask import url_for
from path import path
from sqlalchemy import and_
from genuine_ap.utils import find_model


class SPUMixin(object):

    @property
    def comments(self):
        model = find_model('TB_COMMENT')
        return model.query.filter(model.spu_id == self.id).all()

    def get_nearby_recommendations(self, longitude, lattitude):
        from genuine_ap import apis
        nearby_retailers, distance_list = \
            apis.retailer.find_nearby_retailers(longitude, lattitude)
        spu_id_to_min_distance = {}
        for retailer, distance in zip(nearby_retailers, distance_list):
            for spu in retailer.spu_list:
                if spu.id not in spu_id_to_min_distance or \
                   spu_id_to_min_distance[spu.id] > distance:
                    spu_id_to_min_distance[spu.id] = distance
        try:
            spu_id_to_min_distance.pop(self.id)
        except KeyError:
            pass
        #TODO related kind should be prioritized
        ret = []
        for spu_id, distance in spu_id_to_min_distance.items():
            spu = find_model('TB_SPU').query.get(spu_id)
            ret.append({
                'spu': spu.as_dict(),
                'distance': distance,
                'rating': spu.rating,
                'favor_cnt': len(spu.favors),
            })
        return ret

    def get_same_vendor_recommendations(self, longitude, lattitude):
        model = find_model('TB_SPU')
        cond = and_(model.vendor_id == self.vendor_id,
                    model.id != self.id)
        return model.query.filter(cond).all()

    @property
    def rating(self):
        return sum(c.rating for c in self.comments) / len(self.comments)

    @property
    def pic_url_list(self):
        ret = []
        vendor_dir = 'spu_pics/%s/' % self.vendor_id
        if os.path.exists('static/' + vendor_dir):
            for fname in path('static/' + vendor_dir).files("*.jpg"):
                ret.append(url_for('static',
                                   filename=vendor_dir + path.basename(fname)))
        return ret

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'msrp': self.msrp,
            'vendor': {
                'id': self.vendor.id,
                'name': self.vendor.name,
            },
            'pic_url_list': self.pic_url_list,
        }

    @property
    def favors(self):
        model = find_model('TB_FAVOR')
        return model.query.filter(model.spu_id == self.id).all()
