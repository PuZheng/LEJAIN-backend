# -*- coding: UTF-8 -*-
import shutil
from path import path

from flask import Blueprint, jsonify, request, current_app

from lejian.models import SPUType
from lejian.auth import jwt_required
from lejian.utils import do_commit, snakeize, assert_dir

bp = Blueprint('spu', __name__, static_folder='static',
               template_folder='templates')


@bp.route('/spu-type-list')
@jwt_required
def spu_type_list():
    spu_types = sorted(SPUType.query.all(), key=lambda obj: obj.weight,
                       reverse=True)
    return jsonify({
        'data': [spu_type.__json__() for spu_type in spu_types]
    })


@bp.route('/spu-type/<int:id>', methods=['GET', 'PUT'])
@jwt_required
def spu_type(id):

    spu_type = SPUType.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(spu_type.__json__())

    for k, v in snakeize(request.json).items():
        if k == 'pic_path':
            dir_ = path.joinpath(current_app.config['ASSETS_DIR'],
                                 'spu_type_pics')
            assert_dir(dir_)
            _, ext = path(v).splitext()
            spu_type.pic_path = path.joinpath(dir_, str(spu_type.id) + ext)
            shutil.move(v, spu_type.pic_path)
        elif k == 'enabled':
            setattr(spu_type, k, v == '1')
        else:
            setattr(spu_type, k, v)

    return jsonify(do_commit(spu_type).__json__())
