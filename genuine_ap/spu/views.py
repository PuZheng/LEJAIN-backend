# -*- coding: UTF-8 -*-
from sqlalchemy import and_
from flask import request, jsonify
from flask.ext.login import login_required, current_user

from genuine_ap.models import SPU, Favor
from genuine_ap.utils import do_commit
from . import spu_ws


@spu_ws.route('/favor/<spu_id>', methods=['GET', 'POST'])
@login_required
def favor(spu_id):
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
