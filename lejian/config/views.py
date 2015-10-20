# -*- coding: UTF-8 -*-
from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound
from flask.ext.databrowser import ModelView, col_spec, sa
from flask.ext.databrowser.action import DeleteAction
from flask.ext.babel import lazy_gettext, gettext as _
from genuine_ap.config import config_ws
from genuine_ap.models import Config
from genuine_ap.apis import wraps
from genuine_ap.database import db


@config_ws.route('/config/<opts>')
def config_ws(opts):
    opts = opts.split(',')
    try:
        opts = [wraps(Config.query.filter(Config.name == opt).one()) for opt
                in opts]
    except NoResultFound:
        return "invalid config options", 403
    return jsonify(dict((opt.name, opt.as_dict()) for opt in opts))


class ConfigModelView(ModelView):

    @ModelView.cached
    @property
    def list_columns(self):
        return [
            col_spec.ColSpec('id', _('id')),
            col_spec.ColSpec('name', _('name')),
            col_spec.ColSpec('type_', _('type')),
            col_spec.ColSpec('brief', _('brief')),
            col_spec.ColSpec('value', _('value')),
        ]

    @ModelView.cached
    @property
    def create_columns(self):
        return [
            col_spec.InputColSpec('name', _('name')),
            col_spec.InputColSpec('type_', _('type')),
            col_spec.InputColSpec('brief', _('brief')),
            col_spec.InputColSpec('value', _('value'),
                                  doc=u'若是布尔类型，应当填写1(真)或0(假)'),
        ]

    @ModelView.cached
    @property
    def edit_columns(self):
        return [
            col_spec.InputColSpec('name', _('name')),
            col_spec.InputColSpec('type_', _('type')),
            col_spec.InputColSpec('brief', _('brief')),
            col_spec.InputColSpec('value', _('value'),
                                  doc=u'若是布尔类型，应当填写1(真)或0(假)'),
        ]

    def get_actions(self, processed_objs=None):
        return [DeleteAction(_("remove"))]

config_model_view = ConfigModelView(sa.SAModell(Config, db,
                                                lazy_gettext('Config')))
