#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.endpoints
    ~~~~~~~~~~~~~~~
    This module implements the endpoints
'''

import paxp2
import time
from flask import request, jsonify, current_app as app
from .validation import validate


def index():

    data = {
        'message': 'Welcome to Paxp2',
        'version': paxp2.__version__,
        'timestamp': time.time(),
    }

    return jsonify(data)


@validate('click')
def click():

    res = app.engine.handle(request.json)
    return res


@validate('notice')
def notice():

    data = {"id": "123456"}
    return data

