# -*- coding: UTF-8 -*-
from flask import jsonify, request, render_template, redirect
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash
from flask.ext.login import (current_user, login_user, login_required,
                             logout_user)

from genuine_ap.user import user_ws, user
from genuine_ap.models import User, Group
from genuine_ap import utils, apis, const
from genuine_ap.exceptions import AuthenticateFailure


@user_ws.route('/register', methods=['POST'])
def register_ws():
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
                                password=generate_password_hash(
                                    password, 'pbkdf2:sha256'),
                                group=Group.query.get(const.CUSTOMER_GROUP)))
    user = apis.wraps(user)
    return jsonify(user.as_dict(include_auth_token=True)), 201


@user_ws.route("/login", methods=["POST"])
def login_ws():
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
    return jsonify(user.as_dict(include_auth_token=True))


class LoginForm(Form):

    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "GET":
        if current_user.is_anonymous():
            return render_template("user/login.html", form=form)
        return redirect("/")
    else:
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            try:
                user = apis.user.authenticate(username, password)
            except AuthenticateFailure:
                return render_template("user/login.html",
                                       error=u"用户名或者密码错误", form=form), 403
            if not login_user(user):
                return render_template("user/login.html",
                                       error=u"登陆失败"), 403

            #identity_changed.send(current_app._get_current_object(),
                                  #identity=Identity(user.id))
            return redirect(request.args.get('next') or "/")
        return render_template("user/login.html",
                               error=u"请输入用户名及密码", form=form), 403


@user.route("/logout")
@login_required
def logout():
    try:
        logout_user()
    except Exception:  # in case sesson expire
        pass
    #for key in ('identity.name', 'identity.auth_type'):
        #session.pop(key, None)

    #identity_changed.send(current_app._get_current_object(),
                          #identity=AnonymousIdentity())
    next_url = request.args.get("next", "/")
    return redirect(next_url)
