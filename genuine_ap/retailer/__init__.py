# -*- coding: UTF-8 -*-
from flask import Blueprint

retailer_ws = Blueprint("retailer", __name__, static_folder="static",
                        template_folder="templates")

import genuine_ap.retailer.views
