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
        vendor_dir = posixpath.join('spu_pics', str(self.vendor_id))
        if posixpath.exists(posixpath.join('static', vendor_dir)):
            for fname in path(posixpath.join('static',
                                             vendor_dir)).files("*.jpg"):
                if posixpath.basename(fname) != 'icon.jpg':
                    filename = posixpath.join(vendor_dir, path.basename(fname))
                    ret.append(url_for('static',
                                       filename=filename))
        return ret

    @property
    def icon(self):
        vendor_dir = posixpath.join('spu_pics', str(self.vendor_id))
        if posixpath.exists(posixpath.join('static', vendor_dir)):
            return url_for('static', filename=posixpath.join(vendor_dir,
                                                             'icon.jpg'))
        return ''

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
            'icon': self.icon,
        }

    @property
    def favors(self):
        return Favor.query.filter(Favor.spu_id == self.id).all()


class SPUTypeWrapper(ModelWrapper):

    @property
    def spu_cnt(self):
        return len(self.spu_list)

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
        return '/' + self.pic_path
