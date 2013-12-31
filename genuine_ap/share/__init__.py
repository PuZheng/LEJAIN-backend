#-*- coding:utf-8 -*-
from flask import Blueprint

share = Blueprint("share", import_name=__name__, static_folder="static", template_folder="templates")

from .import views