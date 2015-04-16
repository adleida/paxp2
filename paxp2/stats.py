#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.stats
    ~~~~~~~~~~~
    This module implements the stats
'''

class Stats(object):

    def __init__(self):
        self._stats = {}

    def get_stats(self):
        return self._stats

    def get_value(self, key, default=None):
        return self._stats.get(key, default)

    def set_value(self, key, value):
        self._stats[key] = value

    def inc_value(self, key, count=1, start=0):
        d = self._stats
        d[key] = d.setdefault(key, start) + count

    def max_value(self, key, value):
        self._stats[key] = max(self._stats.setdefault(key, value), value)

    def min_value(self, key, value):
        self._stats[key] = min(self._stats.setdefault(key, value), value)

    def clear_stats(self):
        self._stats.clear()

