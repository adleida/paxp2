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


def check_input(req):

    ok, ex = check_schema(req, 'clk-request')
    if ok:
        return True, None
    else:
        return False, ex


def check_output(res):

    ok, ex = check_schema(res, 'clk-response')
    if ok:
        return True, None
    else:
        return False, ex


def check_token(token, app):

    if app.token:
        return token == app.token
    else:
        return True

