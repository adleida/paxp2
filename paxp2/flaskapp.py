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
from . import bid, endpoints, utils
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

    def run(self, host=None, port=None, debug=None, **options):

        options.setdefault('request_handler', Paxp2WSGIRequestHandler)
        super(App, self).run(host, port, debug, **options)

    def load_config(self):
        
        logger.info('load config')

        self.config.update(self.conf)

    def init_rules(self):

        logger.info('init rules')

        self.add_url_rule(rule='/', view_func=endpoints.index, methods=['GET'])
        self.add_url_rule(rule='/click', view_func=endpoints.click, methods=['POST'])
        self.add_url_rule(rule='/click/', view_func=endpoints.click, methods=['POST'])
        self.add_url_rule(rule='/notice', view_func=endpoints.notice, methods=['POST'])
        self.add_url_rule(rule='/notice/', view_func=endpoints.notice, methods=['POST'])

    def init_engine(self):

        logger.info('init engine')

        try:
            dsp_list = self.config['resources']['dsp']
            if isinstance(dsp_list, str):
                dsp_list = utils.wget_json(dsp_list)
        except:
            logger.error('cannot load dsp-list')
            dsp_list = []
        mgr = bid.BidAgentManager(dsp_list)
        self.engine = bid.BidEngine(mgr)


class Paxp2WSGIRequestHandler(WSGIRequestHandler):

    @property
    def server_version(self):
        return 'Paxp2/%s ' % paxp2.__version__ + \
                super(Paxp2WSGIRequestHandler, self).server_version

