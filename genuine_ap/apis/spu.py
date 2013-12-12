# -*- coding: UTF-8 -*-
import os
import posixpath

from flask import url_for
from path import path
from sqlalchemy import and_
from .model_wrapper import ModelWrapper
from genuine_ap.models import Comment, SPU, Favor
from .model_wrapper import wraps
from . import retailer


class SPUWrapper(ModelWrapper):

    @property
    def comments(self):
        return Comment.query.filter(Comment.spu_id == self.id).all()

    def get_nearby_recommendations(self, longitude, latitude):
        nearby_retailers, distance_list = \
            retailer.find_retailers(longitude, latitude)
        spu_id_to_min_distance = {}
        for retailer_, distance in zip(nearby_retailers, distance_list):
            for spu in retailer_.spu_list:
                if spu.id not in spu_id_to_min_distance:
                    spu_id_to_min_distance[spu.id] = distance
        try:
            spu_id_to_min_distance.pop(self.id)
        except KeyError:
            pass
        #TODO related kind should be prioritized
        ret = []
        for spu_id, distance in spu_id_to_min_distance.items():
            spu = wraps(SPU.query.get(spu_id))
            ret.append({
                'spu': spu.as_dict(),
                'distance': distance,
                'rating': spu.rating,
                'favor_cnt': len(spu.favors),
            })
        return ret

    def get_same_vendor_recommendations(self, longitude, latitude):
        cond = and_(SPU.vendor_id == self.vendor_id,
                    SPU.id != self.id)
        #TODO related kind should be prioritized
        #TODO should be sort by distance
        ret = []
        spu_id_2_distance = retailer.compose_spu_id_2_distance(longitude,
                                                               latitude)
        for spu in SPU.query.filter(cond).all():
            spu = wraps(spu)
            ret.append({
                'spu': spu.as_dict(),
                'distance': spu_id_2_distance.get(spu.id),
                'rating': spu.rating,
                'favor_cnt': len(spu.favors),
            })

        return sorted(ret, key=lambda obj: obj['distance'])


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
            'rating': self.rating,
        }

    @property
    def favors(self):
        return Favor.query.filter(Favor.spu_id == self.id).all()


class SPUTypeWrapper(ModelWrapper):

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time.strftime('%Y-%m-%d'),
            'weight': self.weight,
            'pic_url': self.pic_url
        }

    @property
    def pic_url(self):
        spu_type_logo = posixpath.join('spu_type_pics', str(self.id) + '.jpg')
        if os.path.exists(posixpath.join('static', spu_type_logo)):
            return url_for('static', filename=spu_type_logo)
        return ""
