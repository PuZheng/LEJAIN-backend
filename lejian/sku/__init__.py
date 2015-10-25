# -*- coding: UTF-8 -*-
from flask import Blueprint
from .views import sku_model_view
from genuine_ap.basemain import register_model_view

sku = Blueprint("sku", __name__, static_folder="static",
                template_folder="templates")

for model_view in [sku_model_view]:
    register_model_view(model_view, sku)
