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

# cfg
config = sys.argv[1]
conf = yaml.load(open(config))

# log
log = conf.get('logging', {})
log.setdefault('version', 1)
logging.config.dictConfig(log)

# app
from paxp2.flaskapp import App
app = App(conf=conf)

