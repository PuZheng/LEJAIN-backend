# -*- coding: UTF-8 -*-
from md5 import md5

from flask import jsonify, request

from genuine_ap.user import user_ws
from genuine_ap.models import User, Group
from genuine_ap import utils, apis, const
from genuine_ap.exceptions import AuthenticateFailure


@user_ws.route('/register', methods=['POST'])
def register():
    name = request.args.get("name", type=str)
    password = request.args.get("password", type=str)
    if not name or not password:
        return u"需要name或者password字段", 403

    user = User.query.filter(User.name == name).first()
    if user:
        return jsonify({
            'reason': u'用户名已存在, 请更换注册名。'
        }), 403
    user = utils.do_commit(User(name=name,
                                password=md5(password).hexdigest(),
                                group=Group.query.get(const.CUSTOMER_GROUP)))
    user = apis.wraps(user)
    return jsonify(user.as_dict()), 201


@user_ws.route("/login", methods=["POST"])
def login():
    name = request.args.get("name", type=str)
    password = request.args.get("password", type=str)
    if not name or not password:
        return u"需要name或者password字段", 403
    try:
        user = apis.user.authenticate(name, password)
    except AuthenticateFailure:
        return jsonify({
            'reason': u'用户名或者密码错误'
        }), 403
    return jsonify(user.as_dict())
