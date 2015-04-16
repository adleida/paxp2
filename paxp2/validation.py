#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.validation
    ~~~~~~~~~~~~~~~~
    This module implements the validation
'''

import logging
from .utils import check_schema
from flask import request, jsonify
from functools import wraps


logger = logging.getLogger(__name__)


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
                        res = {'code': 2, 'detail': str(ex_2)}
                else:
                    logger.warn('request is bad')
                    res = {'code': 1, 'detail': str(ex_1)}
            except Exception as ex_3:
                logger.warn('unknown error')
                res = {'code': 3, 'detail': str(ex_3)}

            return jsonify(res)
        
        return decorated

    return fdec

