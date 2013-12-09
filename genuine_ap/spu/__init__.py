# -*- coding: UTF-8 -*-
from flask import Blueprint

spu_ws = Blueprint("spu", __name__, static_folder="static",
                   template_folder="templates")

from genuine_ap.apis.user import load_user_from_token
spu_ws.before_request(load_user_from_token)
import genuine_ap.spu.views
