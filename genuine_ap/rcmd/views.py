# -*- coding: UTF-8 -*-
from flask import jsonify, request
from genuine_ap import utils, models
from . import rcmd_ws


@rcmd_ws.route('/rcmd-list')
def rcmd_list():
    spu_id = request.args['spu_id']
    longitude = request.args.get('longitude', type=float)
    latitude = request.args.get('latitude', type=float)
    kind = request.args['kind']
    if kind not in {'same_vendor', 'nearby', 'same_type'}:
        return '', 404

    spu = utils.get_or_404(models.SPU, spu_id)
    if kind == 'nearby':
        rlist = spu.get_nearby_recommendations(longitude, latitude)
    elif kind == 'same_type':
        rlist = spu.get_same_type_recommendation(longitude, latitude)
    elif kind == 'same_vendor':
        rlist = spu.get_same_vendor_recommendations(longitude, latitude)
    return jsonify({'data': [{
        'spu_id': r['spu']['id'],
        'spu_name': r['spu']['name'],
        'pic_url': r['spu']['icon'],
        'msrp': r['spu']['msrp'],
        'distance': r['distance'] or -1,
        'rating': r['rating'],
        'favor_cnt': r['favor_cnt']
    } for r in rlist]})
