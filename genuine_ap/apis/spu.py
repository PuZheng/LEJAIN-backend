# -*- coding: UTF-8 -*-
import os

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

    def get_nearby_recommendations(self, longitude, lattitude):
        nearby_retailers, distance_list = \
            retailer.find_nearby_retailers(longitude, lattitude)
        spu_id_to_min_distance = {}
        for retailer_, distance in zip(nearby_retailers, distance_list):
            for spu in retailer_.spu_list:
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
            spu = wraps(SPU.query.get(spu_id))
            ret.append({
                'spu': spu.as_dict(),
                'distance': distance,
                'rating': spu.rating,
                'favor_cnt': len(spu.favors),
            })
        return ret

    def get_same_vendor_recommendations(self, longitude, lattitude):
        cond = and_(SPU.vendor_id == self.vendor_id,
                    SPU.id != self.id)
        #TODO related kind should be prioritized
        #TODO should be sort by distance
        ret = []
        for spu in SPU.query.filter(cond).all():
            spu = wraps(spu)
            ret.append({
                'spu': spu.as_dict(),
                'distance': None,
                'rating': spu.rating,
                'favor_cnt': len(spu.favors),
            })
        return ret

    @property
    def rating(self):
        if not self.comments:
            return None
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
            'rating': self.rating,
        }

    @property
    def favors(self):
        return Favor.query.filter(Favor.spu_id == self.id).all()


class CommentWrapper(ModelWrapper):

    def as_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'create_time': self.create_time.strftime('%Y-%m-%d'),
            'spu_id': self.spu_id,
            'spu_name': self.spu.name,
            'user_id': self.user_id,
            'user_name': self.user.name,
            'rating': self.rating
        }
