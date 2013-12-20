# -*- coding: UTF-8 -*-
from flask.ext.databrowser import ModelView, sa, col_spec, extra_widgets
from genuine_ap.database import db
from genuine_ap.models import Vendor
from genuine_ap.apis import wraps
from wtforms import widgets
from flask.ext.databrowser.action import DeleteAction


class VendorModelView(ModelView):

    can_batchly_edit = False

    @property
    def sortable_columns(self):
        return ['id', 'create_time']

    @property
    def list_columns(self):
        return ['id', 'name', 'create_time', 'spu_cnt',
                col_spec.ColSpec('brief',
                                 widget=extra_widgets.PlainText(max_len=24))]

    @property
    def create_columns(self):
        return ['name', col_spec.InputColSpec('brief',
                                              widget=widgets.TextArea())]

    @property
    def edit_columns(self):
        return ['name', col_spec.InputColSpec('brief', widget=widgets.TextArea()),
                col_spec.ColSpec('spu_cnt', label=u'产品数量', )]

    def get_actions(self, processed_objs=None):
        class _DeleteAction(DeleteAction):
            def test_enabled(self, obj):
                return -2 if obj.spu_list else 0

            def get_forbidden_msg_formats(self):
                return {-2: "该厂家下已经存在SPU，所以不能删除!"}

        return [_DeleteAction(u"删除")]

    def expand_model(self, vendor):
        return wraps(vendor)


vendor_model_view = VendorModelView(sa.SAModell(Vendor, db, u"厂家"))
