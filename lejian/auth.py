# -*- coding: UTF-8 -*-
from flask import Blueprint, request, jsonify, current_app, g
import jwt
from sqlalchemy import or_
from werkzeug.security import check_password_hash

from lejian.models import User


bp = Blueprint('auth', __name__, static_folder='static',
               template_folder='templates')


def authenticate(email_or_name, password):
    user = User.query.filter(or_(User.email == email_or_name,
                                 User.name == email_or_name)).first()
    if user and check_password_hash(user.password, password):
        return user


@bp.route('/login', methods=['POST'])
def login():
    email_or_name = request.json.get('emailOrName')
    password = request.json.get('password')

    if not (email_or_name and password):
        return jsonify({
            'reason': '需要邮箱或者用户名, 以及密码字段',
        }), 403

    user = authenticate(email_or_name, password)
    if not user:
        return jsonify({
            'reason': '不正确的用户名和密码'
        }), 403
    user = user.__json__()
    user['token'] = jwt.encode(user, current_app.config['SECRET_KEY'],
                               algorithm='HS256').decode('utf-8')
    return jsonify(user)


class JWTError(Exception):
    pass


def jwt_required(f):

    def _f(*args, **kwargs):
        auth_header_value = request.headers.get('Authorization', None)
        if not auth_header_value:
            raise JWTError('Token missing')
        prefix, token = auth_header_value.split()

        if prefix != 'JWT':
            raise JWTError('Token should be prefixed with JWT')

        try:
            g.current_user = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithm='HS256')
        except jwt.InvalidTokenError as e:
            raise JWTError('Invalid token ' + str(e))
        return f(*args, **kwargs)

    _f.__name__ = f.__name__
    return _f
