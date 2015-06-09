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
from flask import abort, request, jsonify, current_app as app
from .validation import check_token, check_input, check_output, err_msg


def index():

    data = {
        'message': 'Welcome to Paxp2',
        'version': paxp2.__version__,
        'timestamp': time.time(),
    }

    return jsonify(data)


def click():

    if request.method == 'OPTIONS':
        return '', 200, {
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Methods': 'POST'
                        }

    ### TOKEN
    token = request.args.get('token')
    if not check_token(token, app):
        abort(401)

    try:

        ### INPUT
        req = request.get_json()

        ok, err = check_input(req)
        if not ok:
            return jsonify(err_msg(1, err))

        ip = request.remote_addr
        id = str(uuid.uuid4())
        req['id'] = id
        res = app.engine.handle(req)
        app.oplog.log(ip=ip, id=id, req=req, res=res)

        ### OUTPUT
        ok, err = check_output(res)
        if not ok:
            return jsonify(err_msg(2, err))

        return jsonify(res), 200, {'Access-Control-Allow-Origin': '*'}

    except Exception as ex:

        return jsonify(err_msg(-1, ex))


def reload():

    ok = app.engine.reload()
    return jsonify({'reload': ok})


def stats():

    data = app.engine.stats.get_stats()
    return jsonify(data)

