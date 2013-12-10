# -*- coding: UTF-8 -*-
from flask import jsonify, request

from . import tag_ws
from ..models import Tag
from .. import utils


@tag_ws.route('/tag/<id>')
def tag(id):
    tag = utils.get_or_404(Tag, id)
    time_format = '%Y-%m-%d'
    longitude = request.args.get('longitude', 0.0)
    latitude = request.args.get('latitude', 0.0)

    nearby_recommendations_cnt = \
        len(tag.spu.get_nearby_recommendations(longitude, latitude))
    same_vendor_recommendations_cnt = \
        len(tag.spu.get_same_vendor_recommendations(longitude, latitude))
    return jsonify({
        'token': tag.token,
        'sku': {
            'id': tag.sku_id,
            'manufacture_time': tag.sku.manufacture_time.strftime(time_format),
            'expire_time': tag.sku.expire_time.strftime(time_format),
            'spu': tag.spu.as_dict(),
        },
        'create_time': tag.create_time.strftime(time_format),
        'nearby_recommendations_cnt': nearby_recommendations_cnt,
        'same_vendor_recommendations_cnt': same_vendor_recommendations_cnt,
        'comments_cnt': len(tag.spu.comments),
        'favor_cnt': len(tag.spu.favors),
    })
