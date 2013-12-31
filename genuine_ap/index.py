# -*- coding: UTF-8 -*-
from flask import redirect, url_for, render_template
from flask.ext.babel import _
from flask.ext.login import login_required, current_user
from .basemain import app


@app.route('/')
@login_required
def index():
    return redirect(current_user.default_url)


@app.route("/download/<filename>")
def download(filename):
    return redirect(url_for("static", filename=filename))


@app.route('/no_vendor')
def no_vendor():
    return render_template('no_vendor.html', title=_('error'))

@app.route('/no_retailer')
def no_retailer():
    return render_template('no_retailer.html', title=_('error'))
