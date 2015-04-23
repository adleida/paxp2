#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.oplog
    ~~~~~~~~~~~
    This module implements the oplog
'''

import logging
import pymongo
import time


logger = logging.getLogger(__name__)


class OpLogger(object):

    def __init__(self, uri):

        try:
            parsed = pymongo.uri_parser.parse_uri(uri)
            db, coll = parsed['database'], parsed['collection']
            host, port = parsed['nodelist'][0]
            self.mdb = pymongo.MongoClient(host=host, port=port)[db][coll]
            count = self.mdb.find().count()
            logger.info('connect to oplog: %s (%d)', uri, count)
        except:
            self.mdb = None

    def log(self, ip, id, req, res):

        if self.mdb:
            logger.debug('insert oplog')
            self.mdb.insert_one({
                'ip': ip,
                'id': id,
                'rx': req,
                'tx': res,
                'ut': time.time(),
            })

