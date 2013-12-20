# -*- coding: UTF-8 -*-
from flask import jsonify, request, abort

from . import tag_ws
from ..models import SKU
from genuine_ap.apis import wraps


@tag_ws.route('/tag/<id>')
def tag(id):
    sku = SKU.query.filter(SKU.token == id).first()
    if not sku:
        abort(404)
    time_format = '%Y-%m-%d'
    longitude = request.args.get('longitude', type=float)
    latitude = request.args.get('latitude', type=float)

    spu = wraps(sku.spu)
    nearby_recommendations_cnt = \
        len(spu.get_nearby_recommendations(longitude, latitude))
    same_vendor_recommendations_cnt = \
        len(spu.get_same_vendor_recommendations(longitude, latitude))
    return jsonify({
        'token': sku.token,
        'sku': {
            'id': sku.id,
            'manufacture_time': sku.manufacture_date.strftime(time_format),
            'expire_time': sku.expire_date.strftime(time_format),
            'spu': spu.as_dict(),
        },
        'create_time': sku.create_time.strftime(time_format),
        'nearby_recommendations_cnt': nearby_recommendations_cnt,
        'same_vendor_recommendations_cnt': same_vendor_recommendations_cnt,
        'comments_cnt': len(spu.comments),
        'favor_cnt': len(spu.favors),
    })
