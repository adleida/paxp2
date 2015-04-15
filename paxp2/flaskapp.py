#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.flaskapp
    ~~~~~~~~~~~~~~
    This module implements the central WSGI application object as a Flask subclass.
'''


import paxp2
import yaml
from flask import Flask
from paxp2 import endpoints
from werkzeug.serving import WSGIRequestHandler


class App(Flask):

    def __init__(self, **kwargs):
        self.conf = kwargs.pop('conf', {})
        name = kwargs.pop('name', __package__)
        super(App, self).__init__(name, **kwargs)
        self.load_config()
        self.init_rules()

    def run(self, host=None, port=None, debug=None, **options):
        options.setdefault('request_handler', Paxp2WSGIRequestHandler)
        super(App, self).run(host, port, debug, **options)

    def load_config(self):
        self.config.update(self.conf)

    def init_rules(self):
        self.add_url_rule('/', 'index', view_func=endpoints.index, methods=['GET'])
        self.add_url_rule('/click', 'click', view_func=endpoints.click, methods=['POST'])
        self.add_url_rule('/click/', 'click', view_func=endpoints.click, methods=['POST'])
        self.add_url_rule('/notice', 'notice', view_func=endpoints.notice, methods=['POST'])
        self.add_url_rule('/notice/', 'notice', view_func=endpoints.notice, methods=['POST'])


class Paxp2WSGIRequestHandler(WSGIRequestHandler):

    @property
    def server_version(self):
        return 'Paxp2/%s ' % paxp2.__version__ + \
                super(Paxp2WSGIRequestHandler, self).server_version

