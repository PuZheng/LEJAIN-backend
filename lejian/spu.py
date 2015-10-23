# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify

from lejian.models import SPUType

bp = Blueprint('spu', __name__, static_folder='static',
               template_folder='templates')


@bp.route('/spu-type-list')
def spu_type_list():
    spu_types = sorted(SPUType.query.all(), key=lambda obj: obj.weight,
                       reverse=True)
    return jsonify({
        'data': [spu_type.__json__() for spu_type in spu_types]
    })
