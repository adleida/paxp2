#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.oplog
    ~~~~~~~~~~~
    This module implements the oplog
'''

from flask import current_app as app, request
import logging


logger = logging.getLogger(__name__)


def oplog_push(resource, op):

    entry = {
        'rs': resource,
        'id': None,
        'op': op,
        'ip': request.remote_addr
    }

    logger.debug('%s', entry)

