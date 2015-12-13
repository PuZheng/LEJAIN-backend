# -*- coding: UTF-8 -*-
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app

from lejian.models import SKU
from lejian.database import db

bp = Blueprint('sku', __name__, static_folder='static',
               template_folder='templates')


@bp.route('/list.json', methods=['DELETE', 'GET'])
def list_json():

    q = SKU.query
    if request.method == 'DELETE':
        ids = request.args.get('ids', '').split(',')
        for id_ in ids:
            db.session.delete(q.get(id_))
        db.session.commit()
        return jsonify({})

    # GET
    unexpired_only = request.args.get('unexpired_only', type=int)
    if unexpired_only:
        q = q.filter(SKU.expire_date > datetime.today())

    spu_id = request.args.get('spu', type=int)
    if spu_id:
        q = q.filter(SKU.spu_id == spu_id)

    total_cnt = q.count()

    # order by create_time desendentally
    sort_by = request.args.get('sort_by', 'create_time.desc')
    sort_by = sort_by.split('.')
    sort_by = {
        'name': sort_by[0],
        'order': sort_by[1],
    }
    c = getattr(SKU, sort_by['name'])
    if sort_by['order'] == 'desc':
        c = c.desc()

    q = q.order_by(c)

    per_page = request.args.get('per_page', current_app.config['PER_PAGE'],
                                type=int)
    page = request.args.get('page', 1, type=int)

    q = q.offset((page - 1) * per_page).limit(per_page)

    return jsonify({
        'data': q.all(),
        'totalCnt': total_cnt
    })
