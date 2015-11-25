# -*- coding: UTF-8 -*-
import shutil
from path import path
import os
import tempfile

from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import or_

from lejian.database import db
from lejian.models import SPUType, SPU
from lejian.auth import jwt_required
from lejian.utils import do_commit, snakeize, assert_dir, web_api

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
@web_api
def spu_type(id=None):

    if request.method == 'POST':
        data = snakeize(request.json)
        if 'pic_path' in data:
            dir_ = path.joinpath(current_app.config['ASSETS_DIR'],
                                 'spu_type_pics')
            assert_dir(dir_)
            _, ext = path(data['pic_path']).splitext()
            new_pic_path = tempfile.mktemp(suffix=ext, dir=dir_, prefix='')
            shutil.move(data['pic_path'], new_pic_path)
            data['pic_path'] = new_pic_path

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
            _, ext = path(v).splitext()
            spu_type.pic_path = tempfile.mktemp(dir=dir_, prefix='', suffix=ext)
            shutil.move(v, spu_type.pic_path)
        else:
            setattr(spu_type, k, v)

    return jsonify(do_commit(spu_type).__json__())


@bp.route('/spu-list')
@jwt_required
def spu_list():

    q = SPU.query

    vendor_id = request.args.get('vendor_id')
    if vendor_id:
        q = q.filter(SPU.vendor_id == vendor_id)

    spu_type_id = request.args.get('spu_type_id')
    if spu_type_id:
        q = q.filter(SPU.spu_type_id == spu_type_id)

    only_enabled = request.args.get('only_enabled', type=int)
    if only_enabled:
        q = q.filter(SPU.enabled)

    kw = request.args.get('kw')
    if kw:
        q = q.filter(or_(SPU.name.like('%%' + kw + '%%'),
                         SPU.code.like('%%' + kw + '%%')))

    total_cnt = q.count()

    # order by create_time desendentally
    order_by = request.args.get('order_by', 'create_time')
    order_by = getattr(SPU, order_by)
    if request.args.get('desc', 1, type=int):
        order_by = order_by.desc()

    q = q.order_by(order_by)

    per_page = request.args.get('per_page', current_app.config['PER_PAGE'],
                                type=int)
    page = request.args.get('page', 1, type=int)

    q = q.offset((page - 1) * per_page).limit(per_page)

    return jsonify({
        'totalCnt': total_cnt,
        'data': q.all(),
    })
