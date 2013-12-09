# -*- coding: UTF-8 -*-
from flask import request, jsonify
from genuine_ap.models import SPU
from genuine_ap.utils import get_or_404
from . import spu_ws


@spu_ws.route('/comment-list')
def comment_list_view():
    spu = get_or_404(SPU, request.args['spu_id'])
    return jsonify({
        'data': [c.as_dict() for c in spu.comments],
    })
