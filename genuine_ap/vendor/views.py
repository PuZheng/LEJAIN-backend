# -*- coding: UTF-8 -*-
from flask.ext.babel import lazy_gettext, gettext as _
from flask.ext.databrowser import ModelView, sa, extra_widgets, filters
from flask.ext.databrowser.col_spec import ColSpec, InputColSpec
from flask.ext.databrowser.extra_widgets import Link
from flask.ext.principal import Permission
from genuine_ap.database import db
from genuine_ap.models import Vendor, User
from genuine_ap.apis import wraps
from genuine_ap import const
from genuine_ap.spu import spu_model_view
from wtforms import widgets
from flask.ext.databrowser.action import DeleteAction


class VendorModelView(ModelView):

    @property
    def sortable_columns(self):
        return ['id', 'create_time']

    @property
    def list_columns(self):
        return [
            ColSpec('id', _('id')),
            ColSpec('name', _('name')),
            ColSpec('create_time', _('create time')),
            ColSpec('email', _('email')),
            ColSpec('website', _('website')),
            ColSpec('brief', label=_('brief'),
                    widget=extra_widgets.PlainText(max_len=24)),
            ColSpec('spu_cnt', _('spu no.'),
                    formatter=lambda v, obj:
                    (v, spu_model_view.url_for_list(vendor=obj.id)),
                    widget=Link('_blank')),
            ColSpec('administrator', label=_('administrator'))
        ]

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
                         }),
            InputColSpec('administrator', label=_('administrator'),
                         filter_=lambda q: q.filter(User.group_id ==
                                                    const.VENDOR_GROUP))
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
                ColSpec('spu_cnt', label=_('spu no.')),
                InputColSpec('administrator', label=_('administrator'),
                             filter_=lambda q: q.filter(User.group_id ==
                                                        const.VENDOR_GROUP))
                ]

    def get_actions(self, processed_objs=None):
        class _DeleteAction(DeleteAction):
            def test_enabled(self, obj):
                return -2 if obj.spu_list else 0

            def get_forbidden_msg_formats(self):
                return {-2: _("already contains SPU, so can't be removed!")}

        permission = None
        if processed_objs:
            needs = [self.remove_need(obj.id) for obj in processed_objs]
            permission = Permission(*needs).union(
                Permission(self.remove_all_need))

        return [_DeleteAction(_("remove"), permission=permission)]

    @property
    def filters(self):
        return [
            filters.Contains("name", label=_('name'), name=_("contains")),
        ]

    def expand_model(self, vendor):
        return wraps(vendor)


vendor_model_view = VendorModelView(sa.SAModell(Vendor, db,
                                                lazy_gettext("vendor")))
