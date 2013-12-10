# -*- coding: UTF-8 -*-
import sys
from collections import OrderedDict
from flask import request, jsonify, abort

from genuine_ap.models import SPU, SPUType
from genuine_ap.utils import get_or_404
from . import spu_ws
from genuine_ap.apis import wraps
from genuine_ap.apis.retailer import find_retailers


@spu_ws.route('/spu/<int:spu_id>', methods=['GET'])
def spu_view(spu_id):
    longitude = request.args.get('longitude', 0.0)
    latitude = request.args.get('latitude', 0.0)
    spu = get_or_404(SPU, spu_id)
    nearby_recommendations_cnt = \
        len(spu.get_nearby_recommendations(longitude, latitude))
    same_vendor_recommendations_cnt = \
        len(spu.get_same_vendor_recommendations(longitude, latitude))
    return jsonify({
        'spu': spu.as_dict(),
        'nearby_recommendations_cnt': nearby_recommendations_cnt,
        'same_vendor_recommendations_cnt': same_vendor_recommendations_cnt,
        'comments_cnt': len(spu.comments),
    })


@spu_ws.route('/spu-type-list', methods=['GET'])
def spu_type_list():

    spu_types = sorted(SPUType.query.all(), key=lambda obj: obj.weight,
                       reverse=True)
    return jsonify({
        'data': [spu_type.as_dict() for spu_type in wraps(spu_types)]
    })


@spu_ws.route('/spu-list', methods=['GET'])
def spu_list_view():
    # TODO should be paged
    kw = request.args.get('kw')
    spu_type_id = request.args.get('spu_type_id')
    order_by = request.args.get('order_by', 'distance')
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')

    if not (kw or spu_type_id):
        abort(403)

    q = SPU.query
    if spu_type_id:
        filter_cond = SPU.spu_type_id == spu_type_id
    elif kw:
        # TODO use whoosh instead
        filter_cond = SPU.name.contains(kw)
    q = q.filter(filter_cond)

    # TODO a brute force implementation
    nearby_retailers, distance_list = find_retailers(longitude, latitude)
    # spu_id -> (spu, distance)
    spu_id_map = OrderedDict()
    for retailer, distance in zip(nearby_retailers, distance_list):
        for spu in retailer.spu_list:
            if spu.id not in spu_id_map:
                spu_id_map[spu.id] = (spu, distance)

    if order_by == 'distance':
        spu_distance_list = [(wraps(spu),
                              spu_id_map.get(spu.id, [None, None])[1])
                             for spu in q]
        spu_distance_list = sorted(spu_distance_list,
                                   key=lambda x: x[1] if x[1] else sys.maxint)
    elif order_by == 'price':
        spus = q.order_by(SPU.msrp).all()
        spu_distance_list = [(wraps(spu),
                              spu_id_map.get(spu.id, [None, None])[1])
                             for spu in spus]
    elif order_by == 'rating':
        spus = q.order_by(SPU.rating.desc()).all()
        spu_distance_list = [(wraps(spu),
                              spu_id_map.get(spu.id, [None, None])[1])
                             for spu in spus]

    data = []
    for spu, distance in spu_distance_list:
        data.append({
            'spu_id': spu.id,
            'spu_name': spu.name,
            'pic_url': spu.pic_url_list[0],
            'msrp': spu.msrp,
            'rating': spu.rating,
            'favor_cnt': len(spu.favors),
            'distance': distance,
        })
    return jsonify({'data': data})
