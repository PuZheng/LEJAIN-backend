# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify, current_app

from lejian.models import Retailer

bp = Blueprint('retailer', __name__, static_folder='static',
               template_folder='templates')


@bp.route('/list.json')
def list_view():

    q = Retailer.query

    rating = request.args.get('rating')
    if rating:
        q = q.filter(Retailer.rating == rating)

    only_enabled = request.args.get('only_enabled', type=int)
    if only_enabled:
        q = q.filter(Retailer.enabled)

    kw = request.args.get('kw')
    if kw:
        q = q.filter(Retailer.name.like('%%' + kw + '%%'))

    total_cnt = q.count()

    # order by create_time desendentally
    sort_by = request.args.get('sort_by', 'create_time.desc')
    sort_by = sort_by.split('.')
    sort_by = {
        'name': sort_by[0],
        'order': sort_by[1],
    }
    c = getattr(Retailer, sort_by['name'])
    if sort_by['order'] == 'desc':
        c = c.desc()

    q = q.order_by(c)

    per_page = request.args.get('per_page', current_app.config['PER_PAGE'],
                                type=int)
    page = request.args.get('page', 1, type=int)

    q = q.offset((page - 1) * per_page).limit(per_page)

    return jsonify({
        'totalCnt': total_cnt,
        'data': q.all(),
    })


@bp.route('/auto-complete/<kw>')
def auto_complete(kw):

    kw = kw.lower()
    q = Retailer.query.filter(Retailer.name.like('%%%s%%' % kw))
    return jsonify({
        "results": [{
            "title": spu.name
        } for spu in q]
    })


