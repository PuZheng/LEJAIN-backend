# -*- coding: UTF-8 -*-
from flask import Blueprint

user_page = Blueprint("user", __name__, static_folder="static",
                     template_folder="templates")

import genuine_ap.user.views
