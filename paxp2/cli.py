#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.cli
    ~~~~~~~~~
    This module implements the entrypoint.
'''

import argparse
import paxp2
import yaml


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version=paxp2.__version__)
    parser.add_argument('-c', '--config')
    args = parser.parse_args()

    app = paxp2.App(conf={})
    app.run(debug=True)


if __name__ == '__main__':

    main()

