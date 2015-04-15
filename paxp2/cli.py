#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.cli
    ~~~~~~~~~
    This module implements the entrypoint.
'''

import argparse
import logging
import logging.config
import paxp2
import yaml


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version=paxp2.__version__)
    parser.add_argument('-c', '--config')
    args = parser.parse_args()

    conf = yaml.load(open(args.config))

    log = conf.get('logging', {})
    log.setdefault('version', 1)
    logging.config.dictConfig(log)

    app = paxp2.App(conf=conf)
    app.run(debug=conf.get('debug', False))


if __name__ == '__main__':

    main()

