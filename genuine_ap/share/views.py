#-*- coding:utf-8 -*-
from . import share
from flask.templating import render_template
from genuine_ap.models import SPU
from genuine_ap.utils import get_or_404


@share.route("/<id>")
def index(id):
    spu = get_or_404(SPU, id)
    return render_template("share/spu.html", spu=spu)