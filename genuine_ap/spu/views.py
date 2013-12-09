# -*- coding: UTF-8 -*-
from sqlalchemy import and_
from flask import request, jsonify
from flask.ext.login import login_required, current_user

from genuine_ap.models import SPU, Favor
from genuine_ap.utils import do_commit, get_or_404
from . import spu_ws


@spu_ws.route('/favor/<int:spu_id>', methods=['GET', 'POST'])
@login_required
def favor_view(spu_id):
    spu = SPU.query.get_or_404(spu_id)
    favor = Favor.query.filter(and_(Favor.spu_id == spu_id,
                                    Favor.user == current_user)).first()
    if request.method == 'POST':
        if favor:
            return '您已经收藏了该产品!', 403
        favor = do_commit(Favor(spu=spu, user=current_user))
        return jsonify({
            'id': favor.id,
            'create_time': favor.create_time.strftime('%Y-%m-%d')
        })
    else:
        if favor is None:
            return "", 404
        return jsonify({
            'id': favor.id,
            'create_time': favor.create_time.strftime('%Y-%m-%d')
        })


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
