# -*- coding: UTF-8 -*-

from flask import Blueprint

config_ws = Blueprint("config_ws", __name__, static_folder="static",
                      template_folder="templates")

config = Blueprint("config", __name__, static_folder="static",
                   template_folder="templates")

from genuine_ap.config.views import config_model_view
from genuine_ap.basemain import register_model_view
register_model_view(config_model_view, config)
