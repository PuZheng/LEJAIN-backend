# -*- coding: UTF-8 -*-
import os
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("genuine_ap.default_settings")
app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"), silent=True)


def register_views():
    # register web services
    from genuine_ap.tag import tag_page
    app.register_blueprint(tag_page, url_prefix='/tag')
    from genuine_ap.user import user_page
    app.register_blueprint(user_page, url_prefix='/user')
    from genuine_ap.rcmd import rcmd_ws_page
    app.register_blueprint(rcmd_ws_page, url_prefix='/rcmd-ws')
    from genuine_ap.spu import spu_ws
    app.register_blueprint(spu_ws, url_prefix='/spu-ws')
