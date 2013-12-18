# -*- coding: UTF-8 -*-
from flask import redirect
from flask.ext.login import login_required, current_user
from .basemain import app


@app.route('/')
@login_required
def index():
    return redirect(current_user.default_url)
