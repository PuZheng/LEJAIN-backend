# -*- coding: UTF-8 -*-
import random
from flask import url_for

from genuine_ap import models
from genuine_ap.apis import wraps, ModelWrapper


def find_retailers(longitude, latitude, max_distance=1500):
    if not (longitude and latitude):
        return (), ()
    #TODO a dumb implementation
    retailers = models.Retailer.query.all()
    distance_list = []

    for retailer in retailers:
        offset = random.randrange(-10, stop=10) * 0.0001
        retailer.longitude = longitude + offset
        retailer.latitude = latitude + offset
        distance_list.append(abs(offset * 110000))

    #if spu_id:
        #tmp_retailers = []
        #tmp_distance_list = []
        #for retailer, distance in zip(retailers, distance_list):
            #if spu_id in {spu.id for spu in retailer.spu_list}:
                #tmp_retailers.append(retailer)
                #tmp_distance_list.append(distance)
        #retailers = tmp_retailers
        #distance_list = tmp_distance_list

    return wraps(retailers), distance_list


def compose_spu_id_2_distance(longitude, latitude, max_distance=1500):

    retailers, distance_list = find_retailers(longitude, latitude,
                                              max_distance=max_distance)
    print retailers, distance_list
    ret = {}
    for retailer, distance in zip(retailers, distance_list):
        for spu in retailer.spu_list:
            ret[spu.id] = distance
    return ret


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
