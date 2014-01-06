# -*- coding: UTF-8 -*-
from sqlalchemy import and_
from flask.ext.babel import lazy_gettext, gettext as _
from flask.ext.databrowser import ModelView, sa, extra_widgets, filters
from flask.ext.databrowser.col_spec import ColSpec, InputColSpec
from flask.ext.databrowser.extra_widgets import Link
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
            ColSpec('create_time', _('create time'), formatter=lambda v, obj:
                    v.strftime('%Y-%m-%d')),
            ColSpec('email', _('email')),
            ColSpec('website', _('website')),
            ColSpec('brief', label=_('brief'),
                    widget=extra_widgets.PlainText(max_len=24)),
            ColSpec('telephone', _('telephone')),
            ColSpec('address', label=_('address'),
                    widget=extra_widgets.PlainText(max_len=10)),
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
            InputColSpec('telephone', _('telephone')),
            InputColSpec('address', label=_('address')),
            InputColSpec('administrator', label=_('administrator'),
                         filter_=lambda q: q.filter(and_(User.group_id ==
                                                         const.VENDOR_GROUP,
                                                         User.vendor ==
                                                         None)),
                         doc=_('if no account could be selected, make sure '
                               'there\'s a vendor account with no vendor '
                               'assigned'))
        ]

    @property
    def edit_columns(self):
        return [
            InputColSpec('name', _('name')),
            InputColSpec('email', _('email')),
            InputColSpec('website', _('website')),
            InputColSpec('weibo', _('weibo')),
            InputColSpec('weixin_follow_link', _('weixin follow link')),
            InputColSpec('brief', _('brief'), widget=widgets.TextArea(),
                         render_kwargs={
                             'html_params': dict(rows=8, cols=40)
                         }),
            InputColSpec('telephone', _('telephone')),
            InputColSpec('address', label=_('address')),
            ColSpec('spu_cnt', label=_('spu no.')),
        ]

    def get_actions(self, processed_objs=None):
        class _DeleteAction(DeleteAction):

            def test(self, *objs):
                if any(obj.spu_list for obj in objs):
                    return 1
                return super(_DeleteAction, self).test(*objs)

            @property
            def forbidden_msg_formats(self):
                ret = super(_DeleteAction, self).forbidden_msg_formats
                ret[1] = _('vendor %%s already contains SPU, '
                           'can\'t be removed!')
                return ret

        return [_DeleteAction(_("remove"))]

    @property
    def filters(self):
        return [
            filters.Contains("name", self, label=_('name'),
                             name=_("contains")),
        ]

    def expand_model(self, vendor):
        return wraps(vendor)


vendor_model_view = VendorModelView(sa.SAModell(Vendor, db,
                                                lazy_gettext("vendor")))
