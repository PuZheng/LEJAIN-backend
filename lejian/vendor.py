# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify

from lejian.auth import jwt_required
from lejian.models import Vendor

bp = Blueprint('vendor', __name__, static_folder='static',
               template_folder='templates')


@bp.route('/vendor-list')
@jwt_required
def vendor_list():
    return jsonify({
        'data': Vendor.query.all(),
    })
