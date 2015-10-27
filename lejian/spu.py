# -*- coding: UTF-8 -*-
import shutil
from path import path
import os
import tempfile

from flask import Blueprint, jsonify, request, current_app

from lejian.models import SPUType
from lejian.auth import jwt_required
from lejian.utils import do_commit, snakeize, assert_dir

bp = Blueprint('spu', __name__, static_folder='static',
               template_folder='templates')


@bp.route('/spu-type-list')
@jwt_required
def spu_type_list():
    q = SPUType.query
    name = request.args.get('name')
    if name:
        q = q.filter(SPUType.name == name)
    spu_types = sorted(q.all(), key=lambda obj: obj.weight,
                       reverse=True)
    return jsonify({
        'data': [spu_type.__json__() for spu_type in spu_types]
    })


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
