# -*- coding: UTF-8 -*-
from flask import request, jsonify
from . import retailer_ws
from genuine_ap import apis


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
