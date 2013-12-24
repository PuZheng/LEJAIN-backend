# -*- coding: UTF-8 -*-
from flask.ext.babel import lazy_gettext, gettext as _
from flask.ext.databrowser import ModelView, sa, extra_widgets, filters
from flask.ext.databrowser.col_spec import ColSpec, InputColSpec
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
        return [
            ColSpec('id', _('id')),
            ColSpec('name', _('name')),
            ColSpec('create_time', _('create time')),
            ColSpec('spu_cnt', _('spu no.')),
            ColSpec('email', _('email')),
            ColSpec('website', _('website')),
            ColSpec('weibo', _('weibo')),
            ColSpec('weixin_follow_link', _('weixin follow link')),
            ColSpec('brief', label=_('brief'),
                    widget=extra_widgets.PlainText(max_len=24))]

    @property
    def create_columns(self):
        return [
            InputColSpec('name', _('name')),
            InputColSpec('email', _('email')),
            InputColSpec('website', _('website')),
            InputColSpec('weibo', _('weibo')),
            InputColSpec('weixin_follow_link', _('weixin follow link')),
            InputColSpec('brief', label=_('brief'),
                         widget=widgets.TextArea(),
                         render_kwargs={
                             'html_params': dict(rows=8, cols=40)
                         })
        ]

    @property
    def edit_columns(self):
        return [InputColSpec('name', _('name')),
                InputColSpec('email', _('email')),
                InputColSpec('website', _('website')),
                InputColSpec('weibo', _('weibo')),
                InputColSpec('weixin_follow_link', _('weixin follow link')),
                InputColSpec('brief', _('brief'), widget=widgets.TextArea(),
                             render_kwargs={
                                 'html_params': dict(rows=8, cols=40)
                             }),
                ColSpec('spu_cnt', label=_('spu no.'))]

    def get_actions(self, processed_objs=None):
        class _DeleteAction(DeleteAction):
            def test_enabled(self, obj):
                return -2 if obj.spu_list else 0

            def get_forbidden_msg_formats(self):
                return {-2: _("already contains SPU, so can't be removed!")}

        return [_DeleteAction(_("remove"))]

    @property
    def filters(self):
        return [
            filters.Contains("name", label=_('name'), name=_("contains")),
        ]

    def expand_model(self, vendor):
        return wraps(vendor)


vendor_model_view = VendorModelView(sa.SAModell(Vendor, db,
                                                lazy_gettext("vendor")))
