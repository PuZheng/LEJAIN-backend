# -*- coding: UTF-8 -*-
from flask import request, jsonify
from sqlalchemy import and_
from flask.ext.login import login_required, current_user
from . import favor_ws
from genuine_ap.models import Favor, SPU
from genuine_ap.utils import do_commit
from genuine_ap.apis import wraps


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
    favors = wraps(Favor.query.filter(Favor.user == current_user).all())

    ret = {}
    for favor in favors:
        ret.setdefault(favor.spu.spu_type.name, []).append(favor.as_dict())
    return jsonify(ret)
