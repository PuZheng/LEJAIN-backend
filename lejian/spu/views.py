# -*- coding: UTF-8 -*-
import sys
from sqlalchemy import and_
from collections import OrderedDict
from flask import request, jsonify, abort
from flask.ext.babel import lazy_gettext, gettext as _
from flask.ext.databrowser import ModelView, sa, col_spec, filters
from flask.ext.databrowser.extra_widgets import Image, Link
from flask.ext.databrowser.action import DeleteAction
from flask.ext.databrowser.utils import random_str
from flask.ext.login import current_user
from flask.ext.principal import Permission, RoleNeed
import os.path

from genuine_ap.models import SPU, SPUType, Favor, Vendor
from genuine_ap.utils import get_or_404
from . import spu_ws
from genuine_ap.apis import wraps, unwraps
from genuine_ap.apis.retailer import find_retailers
from genuine_ap.database import db
from genuine_ap import const


@spu_ws.route('/spu/<int:spu_id>', methods=['GET'])
def spu_view(spu_id):
    longitude = request.args.get('longitude', type=float)
    latitude = request.args.get('latitude', type=float)
    spu = get_or_404(SPU, spu_id)
    same_type_recommendations_cnt = \
        len(spu.get_same_type_recommendations(longitude, latitude))
    same_vendor_recommendations_cnt = \
        len(spu.get_same_vendor_recommendations(longitude, latitude))
    favored = False
    distance = spu.get_retailer_shortest_distance(longitude, latitude)
    if current_user.is_authenticated():
        q = Favor.query.filter(and_(Favor.spu_id == spu_id,
                                    Favor.user_id == current_user.id))
        favored = q.first() is not None

    return jsonify({
        'spu': spu.as_dict(),
        'same_type_recommendations_cnt': same_type_recommendations_cnt,
        'same_vendor_recommendations_cnt': same_vendor_recommendations_cnt,
        'comments_cnt': len(spu.comment_list),
        'favored': favored,
        'distance': distance,
    })


@spu_ws.route('/spu-type-list', methods=['GET'])
def spu_type_list():

    spu_types = sorted(SPUType.query.all(), key=lambda obj: obj.weight,
                       reverse=True)
    return jsonify({
        'data': [spu_type.as_dict() for spu_type in wraps(spu_types)]
    })


@spu_ws.route('/spu-list', methods=['GET'])
def spu_list_view():
    # TODO should be paged
    kw = request.args.get('kw')
    spu_type_id = request.args.get('spu_type_id', type=int)
    order_by = request.args.get('order_by', 'distance')
    longitude = request.args.get('longitude', type=float)
    latitude = request.args.get('latitude', type=float)

    if not (kw or spu_type_id):
        abort(403)

    q = SPU.query
    if spu_type_id:
        filter_cond = SPU.spu_type_id == spu_type_id
    elif kw:
        # TODO use whoosh instead
        filter_cond = SPU.name.contains(kw)
    q = q.filter(filter_cond)

    # TODO a brute force implementation
    nearby_retailers, distance_list = find_retailers(longitude, latitude)
    # spu_id -> (spu, distance)
    spu_id_map = OrderedDict()
    for retailer, distance in zip(nearby_retailers, distance_list):
        for spu in retailer.spu_list:
            if spu.id not in spu_id_map:
                spu_id_map[spu.id] = (spu, distance)

    if order_by == 'distance':
        spu_distance_list = [(wraps(spu),
                              spu_id_map.get(spu.id, [None, None])[1])
                             for spu in q]
        spu_distance_list = sorted(spu_distance_list,
                                   key=lambda x: x[1] if x[1] else sys.maxint)
    elif order_by == 'price':
        spus = q.order_by(SPU.msrp).all()
        spu_distance_list = [(wraps(spu),
                              spu_id_map.get(spu.id, [None, None])[1])
                             for spu in spus]
    elif order_by == 'rating':
        spus = q.order_by(SPU.rating.desc()).all()
        spu_distance_list = [(wraps(spu),
                              spu_id_map.get(spu.id, [None, None])[1])
                             for spu in spus]

    data = []
    for spu, distance in spu_distance_list:
        data.append({
            'spu_id': spu.id,
            'spu_name': spu.name,
            'pic_url': spu.icon,
            'msrp': spu.msrp,
            'rating': spu.rating,
            'favor_cnt': len(spu.favor_list),
            'distance': distance,
        })
    return jsonify({'data': data})


class SPUTypeModelView(ModelView):

    create_template = edit_template = 'spu/form.html'

    @property
    def sortable_columns(self):
        return ['id', 'weight', 'create_time']

    @property
    def list_columns(self):
        def formatter(v, obj):
            return (v, spu_model_view.url_for_list(spu_type=obj.id))
        return [col_spec.ColSpec('id', label=_('id')),
                col_spec.ColSpec('name', label=_('name')),
                col_spec.ColSpec('weight', label=_('weight')),
                col_spec.ColSpec('create_time', label=_('create time'),
                                 formatter=lambda v, obj:
                                 v.strftime('%Y-%m-%d %H:%M')),
                col_spec.ColSpec('spu_cnt', label=_('spu no.'),
                                 formatter=formatter,
                                 widget=Link(target='_blank')),
                col_spec.ColSpec('pic_url', label=_('logo'),
                                 widget=Image(Image.SMALL))]

    @property
    def create_columns(self):
        save_path = lambda obj, fname: os.path.join('static/spu_type_pics',
                                                    random_str(24) + '.jpg')
        doc = _('size should be %(size)s, only jpeg allowable', size='256x256')
        return [col_spec.InputColSpec('name', label=_('name')),
                col_spec.InputColSpec('weight', label=_('weight')),
                col_spec.FileColSpec('pic_path', label=_('logo'), doc=doc,
                                     save_path=save_path)]

    @property
    def edit_columns(self):
        save_path = lambda obj, fname: os.path.join('static/spu_type_pics',
                                                 random_str(24) + '.jpg')
        doc = _('size should be %(size)s, only jpeg allowable', size='256x256')
        return [
            col_spec.InputColSpec('id', label=_('id'), disabled=True),
            col_spec.InputColSpec('create_time', _('create time'),
                                  disabled=True),
            col_spec.InputColSpec('name', label=_('name')),
            col_spec.InputColSpec('weight', label=_('weight')),
            col_spec.ColSpec('pic_url', label=_('logo'),
                             widget=Image()),
            col_spec.FileColSpec('pic_path', label=_('upload logo'),
                                 save_path=save_path, doc=doc)]

    def expand_model(self, spu_type):
        return wraps(spu_type)

    def get_actions(self, processed_objs=None):
        class _DeleteAction(DeleteAction):

            def test(self, *objs):
                return 1 if any(obj.spu_cnt != 0 for obj in objs) else \
                    super(_DeleteAction, self).test(*objs)

            @property
            def forbidden_msg_formats(self):
                ret = super(_DeleteAction, self).forbidden_msg_formats
                ret[1] = _("%%s already contains SPU, so can't be removed!")
                return ret

        return [_DeleteAction(_("remove"))]

    @property
    def filters(self):
        return [
            filters.Contains("name", self, label=_('name'),
                             name=_("contains")),
        ]


class SPUModelView(ModelView):

    create_template = edit_template = 'spu/form.html'

    def expand_model(self, spu):
        return wraps(spu)

    @property
    def sortable_columns(self):
        return ['id', 'msrp', 'spu_type', 'rating', ('vendor', 'vendor.name')]

    @property
    def default_filters(self):
        if Permission(RoleNeed(const.VENDOR_GROUP)).can():
            return [filters.EqualTo("vendor", self,
                                    value=unwraps(current_user.vendor))]
        return []

    @property
    def list_columns(self):
        def formatter(v, obj):
            from genuine_ap.sku import sku_model_view
            return (v, sku_model_view.url_for_list(spu_id=obj.id))
        ret = [
            col_spec.ColSpec('id', _('id')),
            col_spec.ColSpec('name', _('name')),
            col_spec.ColSpec('msrp', _('msrp')),
            col_spec.ColSpec('vendor', _('vendor')),
            col_spec.ColSpec('spu_type', _('spu type')),
            col_spec.ColSpec('rating', _('rating')),
            col_spec.ColSpec('create_time', _('create time'),
                             formatter=lambda v, obj:
                             v.strftime('%Y-%m-%d %H:%M'))
        ]
        if not Permission(RoleNeed(const.RETAILER_GROUP)).can():
            ret.append(col_spec.ColSpec('sku_cnt', _('sku no.'),
                                        formatter=formatter,
                                        widget=Link(target='_blank')))
        return ret

    @ModelView.cached
    @property
    def create_columns(self):
        doc = _('size should be %(size)s, only jpeg allowable',
                size='1280x720')
        vendor_col_filter = None

        def gen():
            i = 1
            while True:
                yield i
                i += 1
        g = gen()

        def _save_path(obj, fname):
            return str(g.next()) + '.jpg'

        def vendor_col_filter(q):
            if Permission(RoleNeed(const.VENDOR_GROUP)).can():
                return q.filter(Vendor.id == current_user.vendor.id)
            else:
                return q
        return [col_spec.InputColSpec('name', _('name')),
                col_spec.InputColSpec('code', _('code')),
                col_spec.InputColSpec('msrp', _('msrp')),
                col_spec.InputColSpec('vendor', _('vendor'),
                                      filter_=vendor_col_filter),
                col_spec.InputColSpec('spu_type', _('spu type')),
                col_spec.InputColSpec('rating', _('rating')),
                col_spec.FileColSpec('pic_url_list', label=_('upload logos'),
                                     max_num=3, doc=doc, save_path=_save_path)]

    @ModelView.cached
    @property
    def edit_columns(self):
        doc = _('size should be %(size)s, only jpeg allowable',
                size='1280x720')

        def vendor_col_filter(q):
            if Permission(RoleNeed(const.VENDOR_GROUP)).can():
                return q.filter(Vendor.id == current_user.vendor.id)
            else:
                return q

        def gen():
            i = 1
            while True:
                yield i
                i += 1
        g = gen()

        def _save_path(obj, fname):
            return str(g.next()) + '.jpg'
        ret = [
            col_spec.InputColSpec('name', _('name')),
            col_spec.InputColSpec('code', _('code')),
            col_spec.InputColSpec('msrp', _('msrp')),
            col_spec.InputColSpec('spu_type', _('spu type')),
            col_spec.InputColSpec('rating', _('rating')),
            col_spec.InputColSpec('vendor', _('vendor'),
                                  filter_=vendor_col_filter),
            col_spec.ColSpec('pic_url_list', label=_('logos'),
                             widget=Image(size_type=Image.SMALL)),
            col_spec.FileColSpec('pic_url_list', label=_('upload logos'),
                                 max_num=3, doc=doc, save_path=_save_path)]
        return ret

    @property
    def filters(self):
        ret = [
            filters.Contains("name", self, label=_('name'),
                             name=_("contains")),
            filters.EqualTo("spu_type", self, label=_('spu type'),
                            name=_("is")),
            filters.Between('msrp', self, label=_('msrp'),
                            name=_('between')),
        ]
        if not Permission(RoleNeed(const.VENDOR_GROUP)).can():
            ret.append(filters.EqualTo("vendor", self, label=_('vendor'),
                                       name=_("is")))
        return ret

    def get_actions(self, processed_objs=None):

        class _DeleteAction(DeleteAction):

            def test(self, *objs):
                if any(obj.sku_list for obj in objs):
                    return 1
                elif any(obj.comment_list for obj in objs):
                    return 2
                elif any(obj.favor_list for obj in objs):
                    return 3
                return super(_DeleteAction, self).test(*objs)

            @property
            def forbidden_msg_formats(self):
                ret = super(_DeleteAction, self).forbidden_msg_formats
                ret[1] = _('spu %%s already contains sku, can\'t be removed!')
                ret[2] = _('spu %%s already has comments, can\'t be removed!')
                ret[3] = _('spu %%s already has been favored, can\'t be'
                           'removed')
                return ret

        return [_DeleteAction(_("remove"))]

    def on_record_created(self, spu):
        if hasattr(spu, 'temp_pic_url_list'):
            spu.save_pic_url_list(spu.temp_pic_url_list)


spu_type_model_view = SPUTypeModelView(sa.SAModell(SPUType, db,
                                                   lazy_gettext('SPU Type')))
spu_model_view = SPUModelView(sa.SAModell(SPU, db, lazy_gettext("SPU")))
