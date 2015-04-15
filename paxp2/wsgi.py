#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.wsgi
    ~~~~~~~~~~
    This module implements the entrypoint for wsgi.
'''

import paxp2
import sys
import yaml

# FIXME: logging doesn't work

config = sys.argv[1]
conf = yaml.load(open(config))
app = paxp2.App(conf=conf)

