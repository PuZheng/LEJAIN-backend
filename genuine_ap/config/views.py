# -*- coding: UTF-8 -*-
from flask import jsonify
from genuine_ap.config import config_ws


@config_ws.route('/config/<opts>')
def config_ws(opts):
    opts = opts.split(',')
    ret = {
        "share_content": {
            "brief": "分享用语",
            "type": "string",
            "value": "360真品，值得拥有, 查看{{ spu_name }}, 只要{{ spu_msrp }}元，http://127.0.0.1/spu/spu/{{ spu_id }}"
        },
        "spu_share_media": {
            "brief": "是否分享spu图片",
            "type": "bool",
            "value": True,
        }
    }

    return jsonify(ret)
