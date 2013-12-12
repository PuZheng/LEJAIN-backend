# -*- coding: UTF-8 -*-
from flask import request, jsonify
from sqlalchemy import and_
from flask.ext.login import login_required, current_user
from . import favor_ws
from genuine_ap.models import Favor, SPU
from genuine_ap.utils import do_commit
from genuine_ap.apis import wraps, retailer


@favor_ws.route('/favor/<int:spu_id>', methods=['GET', 'POST'])
@login_required
def favor_view(spu_id):
    spu = SPU.query.get_or_404(spu_id)
    favor = wraps(Favor.query.filter(and_(Favor.spu_id == spu_id,
                                          Favor.user == current_user)).first())
    if request.method == 'POST':
        if favor:
            return '您已经收藏了该产品!', 403
        favor = wraps(do_commit(Favor(spu=spu, user=current_user)))
        return jsonify(favor.as_dict())
    else:
        if favor is None:
            return "", 404
        return jsonify(favor.as_dict())


@favor_ws.route('/favors', methods=['GET', 'POST'])
@login_required
def favars_view():
    longitude = request.args.get('longitude', type=float)
    latitude = request.args.get('latitude', type=float)

    favors = wraps(Favor.query.filter(Favor.user == current_user).all())

    ret = {}
    if favors:
        spu_id_2_distance = retailer.compose_spu_id_2_distance(longitude,
                                                               latitude)
        for favor in favors:
            d = favor.as_dict()
            d['distance'] = spu_id_2_distance.get(favor.spu.id)
            ret.setdefault(favor.spu.spu_type.name, []).append(d)

    return jsonify(ret)
