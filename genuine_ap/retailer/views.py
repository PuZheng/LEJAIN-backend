# -*- coding: UTF-8 -*-
from flask import request, jsonify
from wtforms import widgets
from flask.ext.babel import lazy_gettext, gettext as _
from flask.ext.databrowser import ModelView, sa, filters, extra_widgets
from flask.ext.databrowser.col_spec import InputColSpec, ColSpec
from . import retailer_ws
from genuine_ap import apis
from genuine_ap.models import Retailer
from genuine_ap.database import db
from flask.ext.databrowser.action import DeleteAction


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

    can_batchly_edit = False

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
                    formatter=lambda v, obj: v.strftime("%Y-%m-%d %H:%M"))
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
            InputColSpec('spu_list', label=_('spu list'))]

    @property
    def edit_columns(self):
        return [
            InputColSpec('name', label=_('name')),
            InputColSpec('brief', label=_('brief'), widget=widgets.TextArea(),
                         render_kwargs={'html_params':
                                        {'rows': 8, 'cols': 40}}),
            InputColSpec('rating', label=_('rating')),
            InputColSpec('longitude', label=_('longitude')),
            InputColSpec('latitude', label=_('latitude')),
            InputColSpec('address', label=_('address')),
            InputColSpec('spu_list', label=_('spu list'))]

    @property
    def filters(self):
        return [
            filters.Contains("name", label=_('name'), name=_("contains")),
            filters.Contains("address", label=_('address'),
                             name=_("contains")),
        ]

    def get_actions(self, processed_objs=None):
        return [DeleteAction(_('remove'))]

retailer_model_view = RetailerModelView(sa.SAModell(Retailer, db,
                                                    lazy_gettext('Retailer')))
