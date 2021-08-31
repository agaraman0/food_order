from flask import Flask, jsonify
from flask.globals import request
from helper import *

import json

app = Flask(__name__)

@app.route('/can_fulfil_order',methods = ['POST'])
def can_fulfil():

    order_fulfil_request = request.json

    delivery_date = order_fulfil_request.get('delivery_date')
    items_details = order_fulfil_request.get('items')

    order_fulfilment_flag = can_fulfil_order(delivery_date, items_details)
    
    response = { "can_fulfil": order_fulfilment_flag }

    return jsonify(response)


@app.route('/reserve_order',methods = ['POST'])
def reserve_order():
    order_reserve_request = request.json

    delivery_date = order_reserve_request.get('delivery_date')
    items_details = order_reserve_request.get('items')

    can_order_fulfil = can_fulfil_order(delivery_date, items_details)

    if can_order_fulfil:
        update_order_quantities(delivery_date, items_details)
        return {
                    "code": "Success",
                    "data" : {
                    "reserved": True,
                    "message": "Success"
                    }
                }
    return {
                "code": "Success",
                "data" : {
                "reserved": False,
                "message": "Insufficient quantities!"
                }
            }

