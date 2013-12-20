# -*- coding: UTF-8 -*-
from flask.ext.databrowser import ModelView, sa, filters
from genuine_ap.database import db
from genuine_ap.models import SKU


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
            filters.EqualTo("spu.vendor", label=u'商家', name=u"是"),
        ]

sku_model_view = SKUModelView(sa.SAModell(SKU, db, u"SKU"))
