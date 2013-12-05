# -*- coding: UTF-8 -*-
from flask import Blueprint

tag_page = Blueprint("tag", __name__, static_folder="static",
                     template_folder="templates")

import genuine_ap.tag.views
