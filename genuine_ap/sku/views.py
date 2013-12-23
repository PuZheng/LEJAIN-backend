# -*- coding: UTF-8 -*-
from flask.ext.databrowser import ModelView, sa, filters
from genuine_ap.database import db
from genuine_ap.models import SKU
from flask.ext.databrowser.action import DeleteAction


class SKUModelView(ModelView):

    @property
    def sortable_columns(self):
        return ['id', 'manufacture_time', 'expire_time', 'create_time']

    @property
    def list_columns(self):
        return ['id', 'spu', 'spu.vendor', 'manufacture_date', 'expire_date', 'token',
                'create_time']

    @property
    def create_columns(self):
        return ['spu', 'manufacture_date', 'expire_date', 'token']

    @property
    def edit_columns(self):
        return ['spu', 'manufacture_date', 'expire_date', 'token']

    @property
    def batch_edit_columns(self):
        return ['spu', 'manufacture_date', 'expire_date']

    @property
    def filters(self):
        return [
            filters.Contains("spu.name", label=u'产品名称', name=u"包含"),
            filters.EqualTo("spu.vendor", label=u'厂家', name=u"是"),
            filters.EqualTo("spu_id", hidden=True),
            filters.EqualTo("token", label=u'标签', name=u"是"),
        ]

    def get_actions(self, processed_objs=None):
        return [DeleteAction(u"删除")]

sku_model_view = SKUModelView(sa.SAModell(SKU, db, u"SKU"))
