# -*- coding: UTF-8 -*-
from datetime import datetime
from flask import jsonify, request, abort
from sqlalchemy import and_
from flask.ext.login import current_user

from . import tag_ws
from genuine_ap.database import db
from ..models import SKU, User, Favor
from genuine_ap.apis import wraps


@tag_ws.route('/tag/<id>')
def tag(id):
    sku = SKU.query.filter(SKU.token == id).first()
    if not sku:
        abort(404)
    time_format = '%Y-%m-%d %H:%M:%S'
    longitude = request.args.get('longitude', type=float)
    latitude = request.args.get('latitude', type=float)

    spu = wraps(sku.spu)
    same_type_recommendations_cnt = \
        len(spu.get_same_type_recommendations(longitude, latitude))
    same_vendor_recommendations_cnt = \
        len(spu.get_same_vendor_recommendations(longitude, latitude))
    favored = False
    if current_user.is_authenticated():
        q = Favor.query.filter(and_(Favor.spu_id == spu.id,
                                    User.id == current_user.id))
        favored = bool(q.first())
    last_verify_time = sku.last_verify_time
    try:
        sku.last_verify_time = datetime.now()
        sku.verify_count += 1
        db.session.commit()
    except:
        db.session.rollback()

    return jsonify({
        'token': sku.token,
        'verify_cnt': sku.verify_count,
        'last_verify_time': last_verify_time.strftime(time_format) if last_verify_time is not None else None,
        'sku': {
            'id': sku.id,
            'manufacture_time': sku.manufacture_date.strftime(time_format),
            'expire_time': sku.expire_date.strftime(time_format),
            'spu': spu.as_dict(),
        },
        'create_time': sku.create_time.strftime(time_format),
        'same_type_recommendations_cnt': same_type_recommendations_cnt,
        'same_vendor_recommendations_cnt': same_vendor_recommendations_cnt,
        'comments_cnt': len(spu.comment_list),
        'favor_cnt': len(spu.favor_list),
        'favored': favored
    })


@tag_ws.route("/tag-denounce/<id>", methods=["POST"])
def denounce(id):
    #TODO 这是个伪实现
    longitude = request.args.get('longitude', type=float)
    latitude = request.args.get('latitude', type=float)
    reason = request.args.get("reason")
    return ""
