# -*- coding: UTF-8 -*-
from genuine_ap.tag import tag_page


@tag_page.route('/tag/<id>')
def tag(id):
    return "hello"
