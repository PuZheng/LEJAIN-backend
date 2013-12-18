# -*- coding: UTF-8 -*-
import logging
import os
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("genuine_ap.default_settings")
app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"), silent=True)

from flask.ext.babel import Babel
babel = Babel(app)
from flask.ext.login import LoginManager


def init_login():
    from . import models
    from .apis import wraps
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return wraps(models.User.query.get(user_id))
    login_manager.login_view = 'user.login'

init_login()

from flask.ext.databrowser import DataBrowser
from .database import db
# TODO logger need
data_browser = DataBrowser(app, logger=logging.getLogger('timeline'),
                           upload_folder='static/uploads')

from flask.ext.nav_bar import FlaskNavBar
nav_bar = FlaskNavBar(app)


def setup_nav_bar():
    from genuine_ap.spu import spu, spu_type_model_view
    nav_bar.register(spu, name=u'SPU分类',
                     default_url='/spu' + spu_type_model_view.list_view_url,
                     group=u'SPU管理')

setup_nav_bar()


def register_views():
    from . import index
    installed_ws_apps = ['tag', 'user', 'rcmd', 'spu', 'comment', 'retailer',
                         'favor']
    installed_apps = ['user', 'spu']
    # register web services
    for mod in installed_ws_apps:
        pkg = __import__('genuine_ap.' + mod, fromlist=[mod])
        app.register_blueprint(getattr(pkg, mod + '_ws'),
                               url_prefix='/' + mod + '-ws')
    for mod in installed_apps:
        pkg = __import__('genuine_ap.' + mod, fromlist=[mod])
        app.register_blueprint(getattr(pkg, mod),
                               url_prefix='/' + mod)


register_views()


from genuine_ap import utils
utils.assert_dir('static/spu_pics')
utils.assert_dir('static/retailer_pics')
utils.assert_dir('static/spu_type_pics')
utils.assert_dir('static/user_pics')
