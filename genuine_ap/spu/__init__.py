# -*- coding: UTF-8 -*-
from flask import Blueprint

spu_ws = Blueprint("spu", __name__, static_folder="static",
                     template_folder="templates")

import genuine_ap.spu.views
