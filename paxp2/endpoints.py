#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.endpoints
    ~~~~~~~~~~~~~~~
    This module implements the endpoints
'''

import paxp2
import time
import uuid
from flask import request, jsonify, current_app as app
from .validation import validate


def index():

    data = {
        'message': 'Welcome to Paxp2',
        'version': paxp2.__version__,
        'timestamp': time.time(),
    }

    return jsonify(data)


@validate('clk')
def click():

    ip = request.remote_addr
    id = str(uuid.uuid4())

    req = request.get_json()
    req['id'] = id
    res = app.engine.handle(req)
    app.oplog.log(ip=ip, id=id, req=req, res=res)

    return res


def stats():

    data = app.engine.stats.get_stats()
    return jsonify(data)

