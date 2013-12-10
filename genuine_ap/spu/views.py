# -*- coding: UTF-8 -*-
from flask import request, jsonify

from genuine_ap.models import SPU
from genuine_ap.utils import get_or_404
from . import spu_ws


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
