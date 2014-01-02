# -*- coding: UTF-8 -*-
from sqlalchemy import and_
from flask import request, jsonify
from wtforms import widgets
from flask.ext.babel import lazy_gettext, gettext as _
from flask.ext.principal import Permission, RoleNeed
from flask.ext.databrowser import ModelView, sa, filters, extra_widgets
from flask.ext.databrowser.col_spec import InputColSpec, ColSpec
from flask.ext.databrowser.action import DeleteAction

from . import retailer_ws
from genuine_ap import apis, const
from genuine_ap.models import Retailer, User
from genuine_ap.database import db


@retailer_ws.route('/retailer-list')
def retailer_list():

    longitude = request.args.get('longitude', type=float)
    latitude = request.args.get('latitude', type=float)
    spu_id = request.args.get('spu_id', type=int)

    retailers, distance_list = apis.retailer.find_retailers(longitude,
                                                            latitude)

    def _filter_with_spu_id(retailer):
        return not spu_id or (spu_id in {spu.id for spu in retailer.spu_list})

    data = []
    for retailer, distance in zip(retailers, distance_list):
        if _filter_with_spu_id(retailer):
            data.append({
                'retailer': retailer.as_dict(),
                'distance': distance,
            })
    return jsonify({
        'data': data
    })


class RetailerModelView(ModelView):

    @property
    def sortable_columns(self):
        return ['id', 'rating', 'create_time']

    @property
    def list_columns(self):
        return [
            ColSpec('id', label=_('id')),
            ColSpec('name', label=_('name')),
            ColSpec('rating', label=_('rating')),
            ColSpec('address', label=_('address')),
            ColSpec('longitude', label=_('longitude')),
            ColSpec('latitude', label=_('latitude')),
            ColSpec('brief', label=_('brief'),
                    widget=extra_widgets.PlainText(max_len=24)),
            ColSpec('create_time', label=_('create time'),
                    formatter=lambda v, obj: v.strftime("%Y-%m-%d %H:%M")),
            ColSpec('administrator', label=_('administrator')),
        ]

    @property
    def create_columns(self):
        return [
            InputColSpec('name', label=_('name')),
            InputColSpec('brief', label=_('brief'), widget=widgets.TextArea(),
                         render_kwargs={'html_params':
                                        {'rows': 8, 'cols': 40}}),
            InputColSpec('rating', label=_('rating')),
            InputColSpec('longitude', label=_('longitude')),
            InputColSpec('latitude', label=_('latitude')),
            InputColSpec('address', label=_('address')),
            InputColSpec('spu_list', label=_('spu list'),
                         doc=_('you could type to search spu! for Chinese '
                               'character, you could just type the first '
                               'letter of each character to search, for '
                               u'example, "mt" for "茅台"')),
            InputColSpec('administrator', label=_('administrator'),
                         filter_=lambda q: q.filter(and_(User.group_id ==
                                                         const.RETAILER_GROUP,
                                                         User.retailer ==
                                                         None)),
                         doc=_('if no account could be selected, make sure '
                               'there\'s a retailer account with no retailer '
                               'assigned'))
        ]

    @ModelView.cached
    @property
    def edit_columns(self):
        ret = [
            InputColSpec('name', label=_('name')),
            InputColSpec('brief', label=_('brief'), widget=widgets.TextArea(),
                         render_kwargs={'html_params':
                                        {'rows': 8, 'cols': 40}})
        ]
        if Permission(RoleNeed(const.SUPER_ADMIN)).can():
            ret.append(InputColSpec('rating', label=_('rating')))

        ret.extend([
            InputColSpec('longitude', label=_('longitude')),
            InputColSpec('latitude', label=_('latitude')),
            InputColSpec('address', label=_('address')),
            InputColSpec('spu_list', label=_('spu list'),
                         doc=_('you could type to search spu! for Chinese '
                               'character, you could just type the first '
                               'letter of each character to search, for '
                               u'example, "mt" for "茅台"'))
        ])
        if Permission(RoleNeed(const.SUPER_ADMIN)).can():
            cs = InputColSpec('administrator', label=_('administrator'),
                              filter_=lambda q:
                              q.filter(and_(User.group_id ==
                                            const.RETAILER_GROUP,
                                            User.retailer == None)),
                              doc=_('if no account could be selected, make '
                                    'sure there\'s a retailer account with '
                                    'no retailer assigned'))
        elif Permission(RoleNeed(const.RETAILER_GROUP)).can():
            cs = ColSpec('administrator', label=_('administrator'))
        ret.append(cs)
        return ret

    @property
    def filters(self):
        return [
            filters.Contains("name", self, label=_('name'),
                             name=_("contains")),
            filters.Contains("address", self, label=_('address'),
                             name=_("contains")),
        ]

    def get_actions(self, processed_objs=None):
        return [DeleteAction(_('remove'))]

retailer_model_view = RetailerModelView(sa.SAModell(Retailer, db,
                                                    lazy_gettext('Retailer')))
