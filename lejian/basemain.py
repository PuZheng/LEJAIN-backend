# -*- coding: UTF-8 -*-
# import re
# import logging
import os
from flask import (Flask, request, jsonify, g, render_template)
import tempfile
from werkzeug import secure_filename
from sqlalchemy.exc import SQLAlchemyError

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

    @app.errorhandler(Exception)
    def error(error):
        if isinstance(error, SQLAlchemyError):
            from lng_dianping.database import db
            db.session.rollback()
        from werkzeug.debug.tbtools import get_current_traceback

        traceback = get_current_traceback(skip=1, show_hidden_frames=False,
                                          ignore_system_exceptions=True)
        app.logger.error("%s %s" % (request.method, request.url))
        app.logger.error(traceback.plaintext)
        return jsonify({
            'error': traceback.plaintext
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


from json import JSONEncoder
import datetime


class DynamicJSONEncoder(JSONEncoder):
    """
    JSON encoder for custom classes:
        Uses __json__() method if available to prepare the object.
        Especially useful for SQLAlchemy models
    """

    def default(self, o):
        # Custom JSON-encodeable objects
        if hasattr(o, '__json__'):
            return o.__json__()
        if isinstance(o, datetime.datetime):
            return o.isoformat(' ')
        if isinstance(o, datetime.date):
            return o.isoformat()
        if isinstance(o, set):
            return list(o)
        # Default
        return super(DynamicJSONEncoder, self).default(o)

app.json_encoder = DynamicJSONEncoder
