# -*- coding: UTF-8 -*-
# import re
# import logging
import os
from flask import (Flask, request, jsonify)
import tempfile
from werkzeug import secure_filename

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("lejian.default_settings")
app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"), silent=True)


def register_views():
    for mod in ['auth', 'spu']:
        pkg = __import__('lejian.' + mod, fromlist=[mod])
        app.register_blueprint(getattr(pkg, 'bp'),
                               url_prefix='/' + mod)


register_views()


from lejian.auth import JWTError

if not app.debug:
    @app.errorhandler(JWTError)
    def permission_denied(error):
        return jsonify({
            'reason': str(error)
        }), 403

from flask.ext.cors import CORS
CORS(app)


@app.route('/upload', methods=['POST'])
def upload():
    paths = []
    for file_ in request.files.values():
        if file_:
            _, ext = os.path.splitext(
                secure_filename(file_.filename))
            path = tempfile.mktemp(suffix=ext)
            file_.save(path)
            paths.append(path)
    return jsonify({
        'paths': paths
    })
