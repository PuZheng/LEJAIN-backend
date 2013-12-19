# -*- coding: UTF-8 -*-
from flask import Blueprint

spu_ws = Blueprint("spu_ws", __name__, static_folder="static",
                   template_folder="templates")

spu = Blueprint("spu", __name__, static_folder="static",
                template_folder="templates")

from genuine_ap.apis.user import load_user_from_token
spu_ws.before_request(load_user_from_token)
from genuine_ap.spu.views import spu_type_model_view, spu_model_view


from genuine_ap.basemain import data_browser, nav_bar


def _do_register(model_view, bp):
    label = model_view.modell.label
    extra_params = {
        "list_view": {
            "nav_bar": nav_bar,
            'title': label + u'管理'
        },
        "create_view": {
            "nav_bar": nav_bar,
            'title': u'新建' + label
        },
        "form_view": {
            "nav_bar": nav_bar,
            'title': u'编辑' + label
        }

    }
    data_browser.register_model_view(model_view, bp, extra_params)

for model_view in [spu_type_model_view, spu_model_view]:
    _do_register(model_view, spu)
