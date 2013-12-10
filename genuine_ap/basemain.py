# -*- coding: UTF-8 -*-
import os
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("genuine_ap.default_settings")
app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"), silent=True)


from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


def register_views():
    # register web services
    for mod in ['tag', 'user', 'rcmd', 'spu', 'comment', 'retailer']:
        pkg = __import__('genuine_ap.' + mod, fromlist=[mod])
        app.register_blueprint(getattr(pkg, mod + '_ws'),
                               url_prefix='/' + mod + '-ws')

register_views()

from genuine_ap import utils
utils.assert_dir('static/spu_pics')
utils.assert_dir('static/retailer_pics')
