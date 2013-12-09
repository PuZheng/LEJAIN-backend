# -*- coding: UTF-8 -*-
from flask import Blueprint

comment_ws = Blueprint("comment_ws", __name__, static_folder="static",
                       template_folder="templates")

from genuine_ap.apis.user import load_user_from_token
comment_ws.before_request(load_user_from_token)
import genuine_ap.comment.views
