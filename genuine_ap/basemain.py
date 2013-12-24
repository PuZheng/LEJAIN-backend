# -*- coding: UTF-8 -*-
import re
import logging
import os
from flask import Flask, request
from flask.ext.babel import lazy_gettext as _
from flask.ext.upload2 import FlaskUpload

def register_model_view(model_view, bp):
    label = model_view.modell.label
    extra_params = {
        "list_view": {
            "nav_bar": nav_bar,
            'title': _('%(label)s list', label=label),
        },
        "create_view": {
            "nav_bar": nav_bar,
            'title': _('create %(label)s', label=label),
        },
        "form_view": {
            "nav_bar": nav_bar,
            'title': _('edit %(label)s', label=label),
        }

    }
    data_browser.register_model_view(model_view, bp, extra_params)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("genuine_ap.default_settings")
app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"), silent=True)

from flask.ext.babel import Babel
babel = Babel(app)

FlaskUpload(app)


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
    from genuine_ap.spu import spu, spu_type_model_view, spu_model_view
    from genuine_ap.sku import sku, sku_model_view
    from genuine_ap.vendor import vendor, vendor_model_view
    from genuine_ap.retailer import retailer, retailer_model_view
    nav_bar.register(spu, name=u'SPU',
                     default_url='/spu' + spu_model_view.list_view_url,
                     group=u'SPU管理',
                     enabler=lambda nav: re.match('/spu/spu[^t]',
                                                  request.path))
    nav_bar.register(spu, name=u'SPU分类',
                     default_url='/spu' + spu_type_model_view.list_view_url,
                     group=u'SPU管理',
                     enabler=lambda nav:
                     request.path.startswith('/spu/sputype'))
    nav_bar.register(sku, name=u'SKU管理',
                     default_url='/sku' + sku_model_view.list_view_url)
    nav_bar.register(vendor, name=u'厂家管理',
                     default_url='/vendor' + vendor_model_view.list_view_url)
    nav_bar.register(retailer, name=u'商家管理',
                     default_url='/retailer' +
                     retailer_model_view.list_view_url)

setup_nav_bar()


def register_views():
    from . import index
    installed_ws_apps = ['tag', 'user', 'rcmd', 'spu', 'comment', 'retailer',
                         'favor']
    installed_apps = ['user', 'spu', 'sku', 'vendor', 'retailer']
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
