#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.wsgi
    ~~~~~~~~~~
    This module implements the entrypoint for wsgi.
'''

import logging
import logging.config
import sys
import yaml


config = sys.argv[1]
conf = yaml.load(open(config))

log = conf.get('logging', {})
log.setdefault('version', 1)
logging.config.dictConfig(log)

import paxp2
app = paxp2.App(conf=conf)

