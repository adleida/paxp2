#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.flaskapp
    ~~~~~~~~~~~~~~
    This module implements the central WSGI application object as a Flask subclass.
'''


import logging
import paxp2
import yaml
from flask import Flask
from . import bid, endpoints, oplog, utils
from werkzeug.serving import WSGIRequestHandler


logger = logging.getLogger(__name__)


class App(Flask):

    def __init__(self, **kwargs):
        
        logger.info('init app')

        self.conf = kwargs.pop('conf', {})
        name = kwargs.pop('name', __package__)
        super(App, self).__init__(name, **kwargs)
        self.load_config()
        self.init_rules()
        self.init_engine()
        self.init_oplog()

    def run(self, host=None, port=None, debug=None, **options):

        options.setdefault('request_handler', Paxp2WSGIRequestHandler)
        super(App, self).run(host, port, debug, **options)

    def load_config(self):
        
        self.config.update(self.conf)

    def init_rules(self):

        self.add_url_rule(rule='/', view_func=endpoints.index, methods=['GET'])
        self.add_url_rule(rule='/clk', view_func=endpoints.click, methods=['POST'])
        self.add_url_rule(rule='/clk/', view_func=endpoints.click, methods=['POST'])
        self.add_url_rule(rule='/stats', view_func=endpoints.stats, methods=['GET'])
        self.add_url_rule(rule='/stats/', view_func=endpoints.stats, methods=['GET'])
        self.add_url_rule(rule='/reload', view_func=endpoints.reload, methods=['POST'])
        self.add_url_rule(rule='/reload/', view_func=endpoints.reload, methods=['POST'])
        self.error_handler_spec[None][404] = lambda error: endpoints.index()

    def init_engine(self):

        dsp_list = self.config['resources']['dsp']
        adm_url = self.config['resources']['adm']
        mgr = bid.BidAgentManager(dsp_list, adm_url, self.config.get('timeout', 0.5))
        ntr = bid.BidNoticer(self.config.get('notice_timeout', 0.5))
        self.engine = bid.BidEngine(mgr, ntr)

    def init_oplog(self):

        mongo_uri = self.config.get('oplog')
        self.oplog = oplog.OpLogger(mongo_uri)


class Paxp2WSGIRequestHandler(WSGIRequestHandler):

    @property
    def server_version(self):
        return 'Paxp2/%s ' % paxp2.__version__ + \
                super(Paxp2WSGIRequestHandler, self).server_version

