# -*- coding: UTF-8 -*-
from md5 import md5
from flask import _request_ctx_stack, current_app, request
from flask.ext import login
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_

from genuine_ap.basemain import app
from genuine_ap.apis import ModelWrapper, wraps
from genuine_ap.exceptions import AuthenticateFailure
from genuine_ap.models import User


class UserWrapper(login.UserMixin, ModelWrapper):
    """
    a wrapper of the actual user model
    """
    __serializer__ = URLSafeTimedSerializer(
        secret_key=app.config.get('SECRET_KEY'),
        salt=app.config.get('SECURITY_SALT'))

    @property
    def default_url(self):
        return self.group.default_url

    @property
    def permissions(self):
        ret = set()
        for group in self.groups:
            for perm in group.permissions:
                ret.add(perm)
        return ret

    def get_auth_token(self):
        '''
        get the authentiaction token, see
        `https://flask-login.readthedocs.org/en/latest/#flask.ext.login.LoginManager.token_loader`_
        '''
        return self.__serializer__.dumps([self.id, self.name,
                                          self.password])


def get_user(id_):
    if not id_:
        return None
        # TODO 这里需要优化
    try:
        return wraps(User.query.filter(User.id == id_).one())
    except NoResultFound:
        return None


def load_user_from_token():
    ctx = _request_ctx_stack.top
    token = request.args.get('auth_token')
    identity = AnonymousIdentity()
    if token is None:
        ctx.user = current_app.login_manager.anonymous_user()
    else:
        try:
            ctx.user = get_user(UserWrapper.__serializer__.loads(token)[0])
            identity = Identity(ctx.user.id)
            # change identity to reset permissions
        except BadTimeSignature:
            ctx.user = current_app.login_manager.anonymous_user()
    identity_changed.send(current_app._get_current_object(), identity=identity)


def authenticate(name, password):
    """
    authenticate a user, test if name and password mathing
    :return: an authenticated User or None if can't authenticated
    :rtype: User
    :raise: exceptions.AuthenticateFailure
    """
    try:
        filter_cond = and_(User.name == name,
                           User.password == md5(password).hexdigest())
        return UserWrapper(User.query.filter(filter_cond).one())
    except NoResultFound:
        raise AuthenticateFailure("用户名或者密码错误")
