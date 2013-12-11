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
                                                            latitude, spu_id)
    data = []
    for retailer, distance in zip(retailers, distance_list):
        data.append({
            'retailer': retailer.as_dict(),
            'distance': distance,
        })
    return jsonify({
        'data': data
    })
