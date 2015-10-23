# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify, request

from lejian.models import SPUType
from lejian.auth import jwt_required
from lejian.utils import do_commit

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


@bp.route('/spu-type/<int:id>', methods=['PUT'])
@jwt_required
def spu_type(id):

    spu_type = SPUType.query.get_or_404(id)

    for k, v in request.json.items():
        setattr(spu_type, k, v)

    return jsonify(do_commit(spu_type).__json__())
