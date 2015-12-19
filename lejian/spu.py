# -*- coding: UTF-8 -*-
from path import path
import os

from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import or_

from lejian.database import db
from lejian.models import SPUType, SPU
from lejian.auth import jwt_required
from lejian.utils import do_commit, snakeize, assert_dir, formalize_temp_asset

bp = Blueprint('spu', __name__, static_folder='static',
               template_folder='templates')


@bp.route('/spu-type-list', methods=['GET', 'DELETE'])
@jwt_required
def spu_type_list():
    q = SPUType.query
    if request.method == 'GET':
        name = request.args.get('name')
        if name:
            q = q.filter(SPUType.name == name)
        q = q.order_by(SPUType.weight.desc())
        return jsonify({
            'data': q.all(),
        })

    # DELETE
    ids = request.args.get('ids', '').split(',')
    for id_ in ids:
        spu_type = SPUType.query.get(id_)
        if spu_type.pic_path:
            os.unlink(spu_type.pic_path)
        db.session.delete(spu_type)
    db.session.commit()
    return jsonify({})


@bp.route('/spu-type/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@bp.route('/spu-type/', methods=['POST'])
@jwt_required
def spu_type(id=None):

    if request.method == 'POST':
        data = snakeize(request.json)
        if 'pic_path' in data:
            dir_ = path.joinpath(current_app.config['ASSETS_DIR'],
                                 'spu_type_pics')
            assert_dir(dir_)
            data['pic_path'] = formalize_temp_asset(dir_, data['pic_path'])

        return jsonify(do_commit(SPUType(**data)).__json__())

    spu_type = SPUType.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(spu_type.__json__())

    if request.method == 'DELETE':
        id_ = spu_type.id
        if spu_type.pic_path:
            os.unlink(spu_type.pic_path)
        do_commit(spu_type, 'delete')
        return jsonify({
            id: id_
        })

    for k, v in snakeize(request.json).items():
        if k == 'pic_path':
            dir_ = path.joinpath(current_app.config['ASSETS_DIR'],
                                 'spu_type_pics')
            assert_dir(dir_)
            spu_type.pic_path = formalize_temp_asset(dir_, v)
        else:
            setattr(spu_type, k, v)

    return jsonify(do_commit(spu_type).__json__())


def delete_spus(ids):
    for id_ in ids:
        spu = SPU.query.get(id_)
        if spu:
            try:
                if spu.icon:
                    os.unlink(spu.icon)
                if spu.pic_url_list:
                    for pic in spu.pic_url_list:
                        os.unlink(pic)
            except OSError as e:
                current_app.logger.error(e)
            db.session.delete(spu)
    db.session.commit()


@bp.route('/spu-list', methods=['GET', 'DELETE'])
@jwt_required
def spu_list():

    q = SPU.query

    if request.method == 'DELETE':
        ids = request.args.get('ids')
        if ids:
            delete_spus(ids.split(','))
        return jsonify({})

    vendor = request.args.get('vendor')
    if vendor:
        q = q.filter(SPU.vendor_id == vendor)

    spu_type = request.args.get('spu_type')
    if spu_type:
        q = q.filter(SPU.spu_type_id == spu_type)

    rating = request.args.get('rating')
    if rating:
        q = q.filter(SPU.rating == rating)

    only_enabled = request.args.get('only_enabled', type=int)
    if only_enabled:
        q = q.filter(SPU.enabled)

    kw = request.args.get('kw')
    if kw:
        q = q.filter(or_(SPU.name.like('%%' + kw + '%%'),
                         SPU.code.like('%%' + kw + '%%')))

    total_cnt = q.count()

    # order by create_time desendentally
    sort_by = request.args.get('sort_by', 'create_time.desc')
    sort_by = sort_by.split('.')
    sort_by = {
        'name': sort_by[0],
        'order': sort_by[1],
    }
    c = getattr(SPU, sort_by['name'])
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
    return jsonify({
        "results": [{
            "title": spu.name
        } for spu in SPU.query.filter(SPU.name.like('%%%s%%' % kw))]
    })


@bp.route('/spu', methods=["POST"])
@bp.route('/spu/<int:id>', methods=["GET", "PUT"])
@jwt_required
def spu_json(id=None):
    if request.method == 'POST':
        data = snakeize(request.json)
        pic_paths = None
        if 'pic_paths' in data:
            pic_paths = data['pic_paths']
            del data['pic_paths']
        spu = do_commit(SPU(**data))

        if pic_paths:
            dir_ = path.joinpath(current_app.config['ASSETS_DIR'],
                                 'spu_pics', str(spu.id))
            assert_dir(dir_)
            for path_ in pic_paths:
                formalize_temp_asset(dir_, path_)

    else:
        spu = SPU.query.get_or_404(id)
        if request.method == 'PUT':
            for k, v in snakeize(request.json).items():
                if k == 'pic_paths':
                    dir_ = path.joinpath(current_app.config['ASSETS_DIR'],
                                         'spu_pics', str(id))
                    assert_dir(dir_)
                    orig_pic_paths = spu.pic_paths
                    for path_ in v:
                        if path_ not in orig_pic_paths:
                            formalize_temp_asset(dir_, path_)
                    for path_ in orig_pic_paths:
                        if path_ not in v:
                            os.unlink(path_)
                else:
                    setattr(spu, k, v)

    return jsonify(spu.__json__())
