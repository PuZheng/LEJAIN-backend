# -*- coding: UTF-8 -*-
from flask import Blueprint
from genuine_ap.basemain import register_model_view

retailer_ws = Blueprint("retailer-ws", __name__, static_folder="static",
                        template_folder="templates")

from genuine_ap.retailer.views import retailer_model_view

retailer = Blueprint("retailer", __name__, static_folder="static",
                     template_folder="templates")

for model_view in [retailer_model_view]:
    register_model_view(model_view, retailer)
