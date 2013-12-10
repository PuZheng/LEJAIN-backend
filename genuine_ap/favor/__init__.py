# -*- coding: UTF-8 -*-
from flask import Blueprint

favor_ws = Blueprint("favor_ws", __name__, static_folder="static",
                     template_folder="templates")

from genuine_ap.apis.user import load_user_from_token
favor_ws.before_request(load_user_from_token)
import genuine_ap.favor.views
