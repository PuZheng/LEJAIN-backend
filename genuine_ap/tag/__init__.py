# -*- coding: UTF-8 -*-
from flask import Blueprint

tag_ws = Blueprint("tag_ws", __name__, static_folder="static",
                   template_folder="templates")

import genuine_ap.tag.views
from genuine_ap.apis.user import load_user_from_token
tag_ws.before_request(load_user_from_token)
