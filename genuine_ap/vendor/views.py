# -*- coding: UTF-8 -*-
from flask.ext.databrowser import ModelView, sa, col_spec, extra_widgets
from genuine_ap.database import db
from genuine_ap.models import Vendor
from wtforms import widgets


class VendorModelView(ModelView):

    can_batchly_edit = False

    @property
    def sortable_columns(self):
        return ['id', 'create_time']

    @property
    def list_columns(self):
        return ['id', 'name', 'create_time',
                col_spec.ColSpec('brief',
                                 widget=extra_widgets.PlainText(max_len=24))]

    @property
    def create_columns(self):
        return ['name', col_spec.InputColSpec('brief',
                                              widget=widgets.TextArea())]

    @property
    def edit_columns(self):
        return ['name', col_spec.ColSpec('brief', widget=widgets.TextArea())]


vendor_model_view = VendorModelView(sa.SAModell(Vendor, db, u"厂家"))
