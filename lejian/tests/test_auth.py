# -*- coding: UTF-8 -*-
import os
import tempfile
import json

from lejian.basemain import app
from lejian.tools.init_db import init_db
from lejian.tools.gen_roles import gen_roles

client = app.test_client()

db_file = tempfile.mkstemp(dir='./')[1]


def setup_module(module):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
    app.config['SQLALCHEMY_ECHO'] = False
    init_db()
    gen_roles()


def teardown_module(module):
    os.unlink(db_file)


def test_login():
    from flask import url_for

    with app.test_request_context():
        data = json.dumps({
            'email_or_name': 'admin@lejian.com',
            'password': 'admin'
        })
        rv = client.post(url_for('auth.login'), data=data,
                         content_type='application/json',
                         content_length=len(data))
        assert(rv.status_code == 200)
        response = json.loads(rv.data.decode('utf-8'))
        assert('token' in response)
