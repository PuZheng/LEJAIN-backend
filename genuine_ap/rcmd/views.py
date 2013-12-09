# -*- coding: UTF-8 -*-
from flask import jsonify, request
from genuine_ap import utils, models
from . import rcmd_ws_page


@rcmd_ws_page.route('/rcmd-list')
def rcmd_list():
    spu_id = request.args['spu_id']
    longitue = request.args.get('longitude', None)
    latitude = request.args.get('latitude', None)
    kind = request.args['kind']
    if kind not in {'same_vendor', 'nearby'}:
        return '', 404

    spu = utils.get_or_404(models.SPU, spu_id)
    if kind == 'nearby':
        rlist = spu.get_nearby_recommendations(longitue, latitude)
    elif kind == 'same_vendor':
        rlist = spu.get_same_vendor_recommendations(longitue, latitude)
    return jsonify({'data': [{
        'spu_id': r['spu']['id'],
        'spu_name': r['spu']['name'],
        'pic_url': r['spu']['pic_url_list'][0],
        'msrp': r['spu']['msrp'],
        'distance': r['distance'],
        'rating': r['rating'],
        'favor_cnt': r['favor_cnt']
    } for r in rlist]})
