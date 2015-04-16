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
import yaml


def main():

    import paxp2

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version=paxp2.__version__)
    parser.add_argument('-c', '--config')
    args = parser.parse_args()

    conf = yaml.load(open(args.config))

    log = conf.get('logging', {})
    log.setdefault('version', 1)
    logging.config.dictConfig(log)

    from paxp2.flaskapp import App

    host, port = conf.get('bind', '127.0.0.0:5000').split(':')
    app = App(conf=conf)
    app.run(host=host, port=int(port), debug=conf.get('debug', False))


if __name__ == '__main__':

    main()

