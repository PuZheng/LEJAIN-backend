# -*- coding: UTF-8 -*-
from flask import request, jsonify
from wtforms import widgets
from flask.ext.databrowser import ModelView, sa, col_spec
from . import retailer_ws
from genuine_ap import apis
from genuine_ap.models import Retailer
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

    can_batchly_edit = False

    @property
    def sortable_columns(self):
        return ['id', 'rating', 'create_time']

    @property
    def list_columns(self):
        return ['id', 'name', 'rating', 'address', 'longitude', 'latitude',
                'brief']

    @property
    def create_columns(self):
        return ['name', col_spec.InputColSpec('brief',
                                              widget=widgets.TextArea()),
                'rating', 'longitude', 'latitude', 'address', 'spu_list']

    @property
    def edit_columns(self):
        return ['name', col_spec.InputColSpec('brief',
                                              widget=widgets.TextArea()),
                'rating', 'longitude', 'latitude', 'address', 'spu_list']


retailer_model_view = RetailerModelView(sa.SAModell(Retailer, db, u"商家"))
