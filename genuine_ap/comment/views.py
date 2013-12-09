# -*- coding: UTF-8 -*-
from flask import request, jsonify, abort
from wtforms import (TextField, Form, IntegerField, FloatField, validators,
                     ValidationError)
from flask.ext.login import current_user

from genuine_ap.models import Comment, SPU
from genuine_ap.utils import get_or_404, do_commit
from genuine_ap.apis import wraps
from . import comment_ws


@comment_ws.route('/comment-list')
def comment_list_view():
    spu = get_or_404(SPU, request.args['spu_id'])
    return jsonify({
        'data': [c.as_dict() for c in spu.comments],
    })


@comment_ws.route('/comment', methods=['POST'])
@comment_ws.route('/comment/<int:comment_id>', methods=['GET'])
def comment_view(comment_id=None):

    if request.method == 'GET':
        comment = get_or_404(Comment, comment_id)
    else:  # POST
        class _Form(Form):
            spu_id = IntegerField('spu_id',
                                  validators=[validators.DataRequired()])
            content = TextField('content',
                                validators=[validators.DataRequired()])
            rating = FloatField('rating',
                                validators=[validators.DataRequired()])

            def validate_spu_id(self, field):
                self.spu = wraps(SPU.query.get(field.data))
                if not self.spu:
                    raise ValidationError(u"没有该产品id: " + str(field.data))

        if not current_user.is_authenticated():
            abort(401)
        form = _Form(request.args)
        if not form.validate():
            return jsonify({
                'reason': str(form.errors)
            }), 403
        comment = wraps(do_commit(Comment(spu=form.spu, user=current_user,
                                          rating=form.rating.data,
                                          content=form.content.data)))
    return jsonify(comment.as_dict())
