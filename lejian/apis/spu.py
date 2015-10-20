# -*- coding: UTF-8 -*-
import os.path

from flask import url_for
from sqlalchemy import and_
import sys
from .model_wrapper import ModelWrapper
from genuine_ap.models import SPU
from .model_wrapper import wraps
from . import retailer


class SPUWrapper(ModelWrapper):
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
                'favor_cnt': len(spu.favor_list),
            })
        return ret

    @property
    def sku_cnt(self):
        return len(self.sku_list)

    def get_same_vendor_recommendations(self, longitude, latitude):
        cond = and_(SPU.vendor_id == self.vendor_id,
                    SPU.id != self.id)
        return self._get_recommendations(cond, longitude, latitude)

    def get_same_type_recommendations(self, longitude, latitude):
        cond = and_(SPU.spu_type_id == self.spu_type_id,
                    SPU.id != self.id)
        return self._get_recommendations(cond, longitude, latitude)

    def get_retailer_shortest_distance(self, longitude, latitude):
        recommendations = self._get_recommendations(SPU.id == self.id,
                                                    longitude, latitude)
        return recommendations[0]["distance"] if recommendations else -1

    @property
    def icon(self):
        spu_dir = os.path.join('spu_pics', str(self.vendor_id), str(self.id))
        if os.path.exists(os.path.join('static', spu_dir)):
            filename = os.path.join(spu_dir, 'icon.jpg')
            if sys.platform.startswith("win32"):
                filename = filename.replace(os.path.sep, os.path.altsep)
            return url_for('static', filename=filename)
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
                'tel': self.vendor.telephone,
                'website': self.vendor.website.url if self.vendor.website else "",
                'address': self.vendor.address,
                'weibo': self.vendor.weibo,
                'weibo_link': self.vendor.weibo_link.url if self.vendor.weibo_link else "",
                'weixin': self.vendor.weixin_number
            },
            'pic_url_list': self.pic_url_list,
            'rating': self.rating,
            'icon': self.icon,
        }

    def _get_recommendations(self, cond, longitude, latitude):
        #TODO related kind should be prioritized
        #TODO should be sort by distance
        ret = []
        spu_id_2_distance = retailer.compose_spu_id_2_distance(longitude,
                                                               latitude)
        for spu in SPU.query.filter(cond).all():
            spu = wraps(spu)
            ret.append({
                'spu': spu.as_dict(),
                'distance': spu_id_2_distance.get(spu.id, -1),
                'rating': spu.rating,
                'favor_cnt': len(spu.favor_list),
            })
        return sorted(ret, key=lambda obj: obj['distance'])


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
