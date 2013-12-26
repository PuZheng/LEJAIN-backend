# -*- coding: UTF-8 -*-
from flask.ext.babel import gettext as _
from flask.ext.databrowser import ModelView, sa, filters
from flask.ext.databrowser.col_spec import ColSpec
from genuine_ap.database import db
from genuine_ap.models import SKU
from flask.ext.databrowser.action import DeleteAction


class SKUModelView(ModelView):

    @property
    def sortable_columns(self):
        return ['id', 'manufacture_time', 'expire_time', 'create_time']

    @property
    def list_columns(self):
        return [ColSpec('id', _('id')),
                ColSpec('spu', _('spu')),
                ColSpec('spu.vendor', _('vendor')),
                ColSpec('manufacture_date', _('manufacture date')),
                ColSpec('expire_date', _('expire date')),
                ColSpec('token', _('token')),
                ColSpec('create_time', _('create time'))]

    @property
    def create_columns(self):
        return [
            ColSpec('spu', _('spu')),
            ColSpec('manufacture_date', _('manufacture date')),
            ColSpec('expire_date', _('expire date')),
            ColSpec('token', _('token'))
        ]

    @property
    def edit_columns(self):
        return [
            ColSpec('spu', _('spu')),
            ColSpec('manufacture_date', _('manufacture date')),
            ColSpec('expire_date', _('expire date')),
            ColSpec('token', _('token'))
        ]

    @property
    def batch_edit_columns(self):
        return [ColSpec('spu', _('spu')),
                ColSpec('manufacture_date', _('manufacture date')),
                ColSpec('expire_date', _('expire date'))]

    @property
    def filters(self):
        return [
            filters.Contains("spu.name", label=_('spu name'),
                             name=_("contains")),
            filters.EqualTo("spu.vendor", label=_('vendor'), name=_("is")),
            filters.EqualTo("spu_id", hidden=True),
            filters.EqualTo("token", label=_('token'), name=_("is")),
        ]

    def get_actions(self, processed_objs=None):
        return [DeleteAction(_("remove"))]

sku_model_view = SKUModelView(sa.SAModell(SKU, db, u"SKU"))
