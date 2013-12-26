# -*- coding: UTF-8 -*-
from flask.ext.babel import gettext as _
from flask.ext.databrowser import ModelView, sa, filters
from flask.ext.databrowser.col_spec import ColSpec, InputColSpec
from flask.ext.databrowser.action import DeleteAction
from flask.ext.principal import Permission, RoleNeed
from flask.ext.login import current_user
from genuine_ap.database import db
from genuine_ap.models import SKU, Vendor
from genuine_ap import const
from genuine_ap.apis import unwraps
from genuine_ap.spu import spu_model_view


class SKUModelView(ModelView):

    def try_edit(self, objs=None):
        for obj in objs:
            Permission(spu_model_view.edit_need(obj.spu.id)).test()

    @property
    def can_batchly_edit(self):
        return Permission(RoleNeed(const.SUPER_ADMIN)).can()

    @property
    def sortable_columns(self):
        return ['id', 'manufacture_time', 'expire_time', 'create_time']

    @property
    def default_filters(self):
        if Permission(RoleNeed(const.VENDOR_GROUP)).can():
            return [filters.EqualTo('spu.vendor',
                                    value=unwraps(current_user.vendor))]
        return []

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
        filter_ = None
        if Permission(RoleNeed(const.VENDOR_GROUP)).can():
            filter_ = lambda q: q.filter(Vendor.id ==
                                         current_user.vendor.id).join(Vendor)
        return [
            InputColSpec('spu', _('spu'), filter_=filter_),
            InputColSpec('manufacture_date', _('manufacture date')),
            InputColSpec('expire_date', _('expire date')),
            InputColSpec('token', _('token'))
        ]

    @property
    def edit_columns(self):
        filter_ = None
        if Permission(RoleNeed(const.VENDOR_GROUP)).can():
            filter_ = lambda q: q.filter(Vendor.id ==
                                         current_user.vendor.id).join(Vendor)
        return [
            InputColSpec('spu', _('spu'), filter_=filter_),
            InputColSpec('manufacture_date', _('manufacture date')),
            InputColSpec('expire_date', _('expire date')),
            InputColSpec('token', _('token'))
        ]

    @property
    def batch_edit_columns(self):
        return [ColSpec('spu', _('spu')),
                ColSpec('manufacture_date', _('manufacture date')),
                ColSpec('expire_date', _('expire date'))]

    @property
    def filters(self):
        ret = [
            filters.Contains("spu.name", label=_('spu name'),
                             name=_("contains")),
            filters.EqualTo("spu_id", hidden=True),
            filters.EqualTo("token", label=_('token'), name=_("is")),
        ]
        if Permission(RoleNeed(const.SUPER_ADMIN)).can():
            ret.append(filters.EqualTo("spu.vendor", label=_('vendor'),
                                       name=_("is")))
        return ret

    def get_actions(self, processed_objs=None):
        permission = None
        if processed_objs:
            needs = [spu_model_view.remove_need(obj.spu.id) for obj in
                     processed_objs]
            permission = Permission(*needs).union(
                Permission(self.remove_all_need))
        return [DeleteAction(_("remove"), permission=permission)]

sku_model_view = SKUModelView(sa.SAModell(SKU, db, u"SKU"))
