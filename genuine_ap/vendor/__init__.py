# -*- coding: UTF-8 -*-
from flask import Blueprint
from .views import vendor_model_view
from genuine_ap.basemain import register_model_view

vendor = Blueprint("vendor", __name__, static_folder="static",
                   template_folder="templates")

for model_view in [vendor_model_view]:
    register_model_view(model_view, vendor)
