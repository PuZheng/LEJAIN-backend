# -*- coding: UTF-8 -*-
from flask import redirect, url_for
from flask.ext.login import login_required, current_user
from .basemain import app


@app.route('/')
@login_required
def index():
    return redirect(current_user.default_url)


@app.route("/download/<filename>")
def download(filename):
    return redirect(url_for("static", filename=filename))