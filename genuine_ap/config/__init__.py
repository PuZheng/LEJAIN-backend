# -*- coding: UTF-8 -*-

from flask import Blueprint

config_ws = Blueprint("config_ws", __name__, static_folder="static",
                    template_folder="templates")

config = Blueprint("config", __name__, static_folder="static",
                 template_folder="templates")

import genuine_ap.config.views
