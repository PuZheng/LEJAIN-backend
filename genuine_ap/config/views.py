# -*- coding: UTF-8 -*-
from flask import jsonify
from genuine_ap.config import config_ws
from genuine_ap.models import Config
from genuine_ap.apis import wraps
from sqlalchemy.orm.exc import NoResultFound


@config_ws.route('/config/<opts>')
def config_ws(opts):
    opts = opts.split(',')
    try:
        opts = [wraps(Config.query.filter(Config.name == opt).one()) for opt
                in opts]
    except NoResultFound:
        return "invalid config options", 403
    return jsonify(dict((opt.name, opt.as_dict()) for opt in opts))
