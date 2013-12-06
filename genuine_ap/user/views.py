# -*- coding: UTF-8 -*-
from flask import jsonify, request
from sqlalchemy import and_

from genuine_ap.user import user_page
from genuine_ap.models import User, SPU, Favor
from genuine_ap import utils

@user_page.route('/favor/<spu_id>', methods=['GET', 'POST'])
def favor(spu_id):
    user_id = request.args['user_id']
    user = User.query.filter(User.id==user_id).one()
    spu = SPU.query.get_or_404(spu_id)
    if request.method == 'POST':
        favor = utils.do_commit(Favor(spu=spu, user=user))
        return str(favor.id)
    else:
        favor = Favor.query.filter(and_(Favor.spu_id==spu_id, 
            Favor.user_id==user_id)).first()
        if favor is None:
            return "", 404
        return jsonify({
            'id': favor.id,
            'create_time': favor.create_time.strftime('%Y-%m-%d')
        })
