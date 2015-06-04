#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.validation
    ~~~~~~~~~~~~~~~~
    This module implements the validation
'''

import logging
from .utils import check_schema
from .errorcode import ERROR_CODE_TABLE
from flask import request, jsonify
from functools import wraps


logger = logging.getLogger(__name__)


def err_msg(code, ex=None):

    msg = {
        "adm": [],
        "is_test": 0,
        "error": {
            "code": code,
            "detail": ERROR_CODE_TABLE.get(code, '')
        }
    }

    if ex:
        msg['error']['detail'] += '({})'.format(ex)

    return msg


def validate(schema):

    req_schema = '{}-request'.format(schema)
    res_schema = '{}-response'.format(schema)

    def fdec(f):

        @wraps(f)
        def decorated(*args, **kwargs):

            try:
                req = request.get_json()
                ok_1, ex_1 = check_schema(req, req_schema)
                if ok_1:
                    logger.debug('requset is ok')
                    res = f(*args, **kwargs)
                    ok_2, ex_2 = check_schema(res, res_schema)
                    if ok_2:
                        logger.debug('response is ok')
                    else:
                        logger.warn('response is bad')
                        res = err_msg(2, ex_2)
                else:
                    logger.warn('request is bad')
                    res = err_msg(1, ex_1)
            except Exception as ex_3:
                logger.warn('unknown error: %s', ex_3)
                res = err_msg(-1, ex_3)

            return jsonify(res), 200, {'Access-Control-Allow-Origin': '*'}
        
        return decorated

    return fdec

