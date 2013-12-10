# -*- coding: UTF-8 -*-
from flask import Blueprint

rcmd_ws = Blueprint("rcmd_ws", __name__, static_folder="static",
                     template_folder="templates")

import genuine_ap.rcmd.views
