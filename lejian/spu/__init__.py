# -*- coding: UTF-8 -*-
from flask import Blueprint

spu_ws = Blueprint("spu_ws", __name__, static_folder="static",
                   template_folder="templates")

spu = Blueprint("spu", __name__, static_folder="static",
                template_folder="templates")

from genuine_ap.apis.user import load_user_from_token
spu_ws.before_request(load_user_from_token)
from genuine_ap.spu.views import spu_type_model_view, spu_model_view


from genuine_ap.basemain import register_model_view
for model_view in [spu_type_model_view, spu_model_view]:
    register_model_view(model_view, spu)
