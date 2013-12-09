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
    from genuine_ap.tag import tag_page
    app.register_blueprint(tag_page, url_prefix='/tag')
    from genuine_ap.user import user_ws
    app.register_blueprint(user_ws, url_prefix='/user-ws')
    from genuine_ap.rcmd import rcmd_ws_page
    app.register_blueprint(rcmd_ws_page, url_prefix='/rcmd-ws')
    from genuine_ap.spu import spu_ws
    app.register_blueprint(spu_ws, url_prefix='/spu-ws')
    from genuine_ap.comment import comment_ws
    app.register_blueprint(comment_ws, url_prefix='/comment-ws')
