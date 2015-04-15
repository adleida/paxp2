#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.endpoints
    ~~~~~~~~~~~~~~~
    This module implements the endpoints
'''

import paxp2
import time
from flask import jsonify


def index():

    data = {
        'message': 'Welcome to Paxp2',
        'version': paxp2.__version__,
        'timestamp': time.time(),
    }

    return jsonify(data)


def click():

    data = {}
    return jsonify(data)


def notice():

    data = {}
    return jsonify(data)

