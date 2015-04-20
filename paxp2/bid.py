#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.bid
    ~~~~~~~~~
    This module implements the bidding logic
'''

import copy
import logging
import requests
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from toolz import dicttoolz
from .stats import Stats
from . import utils


logger = logging.getLogger(__name__)


class BidMessage(object):

    @staticmethod
    def make(request_data):
        return BidMessage(request_data)

    def __init__(self, request_data):

        if 'id' in request_data:
            self.uuid = request_data['id']
        else:
            self.uuid = request_data['id'] = str(uuid.uuid4())

        self.request_data = request_data
        self.start_time = time.time()
        self.freezed = False
        self.results = {}
        self.winners = self.losers = set()

    def freeze(self):
        self.freezed = True

    def add_result(self, result):
        if not self.freezed:
            did = result['did']
            self.results[did] = result

    def get_results(self):
        return self.results

    def set_response(self, response_data):
        self.response_data = response_data
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

    def set_decision(self, winners, losers):
        self.winners = winners
        self.losers = losers

    def get_decision(self):
        return self.winners, self.losers

    def set_empty_response(self):
        empty_response_data = {'adm': [], 'is_test': 0}
        self.set_response(empty_response_data)

    def get_response(self):
        return self.response_data

    def get_request(self):
        return self.request_data

    def __str__(self):
        try:
            return '''
            ======BidMsg======
            uuid:     {}
            request:  {}
            response: {}
            ------------------
            start:    {}
            end:      {}
            elapsed:  {:.2f} ms
            ==================
            '''.format(self.uuid, self.request_data, self.response_data, self.start_time, self.end_time, self.elapsed_time*1000)
        except:
            return '''
            ======BidMsg======
            uuid:     {}
            request:  {}
            ------------------
            start:    {}
            ==================
            '''.format(self.uuid, self.request_data, self.start_time)


class BidAgent(object):

    def __init__(self, mgr, id, name, burl):

        self.mgr = mgr
        self.id = id
        self.name = name
        self.burl = burl
        logger.info('init bid-agent: %s:::%s:::%s', self.id, self.name, self.burl)

    def send(self, msg):

        logger.debug('send bid-request to: %s', self.id)
        try:
            data = msg.get_request()
            result = self._send(data)
            self._check(result, msg)
            msg.add_result(result)
            logger.debug('recv bid-response from: %s (ok)', self.id)
        except Exception as ex:
            logger.warning('recv bid-response from: %s (%s)', self.id, ex)

    def _send(self, data):

        try:
            return requests.post(self.burl, json=data, timeout=self.mgr.timeout).json()
        except:
            raise Exception('network error')

    def _check(self, data, msg):

        if not isinstance(data, dict):
            raise Exception('not json')

        if not data.get('did') == self.id:
            raise Exception('"did" mismatch')

        if not data.get('id') == msg.uuid:
            raise Exception('"id" mismatch')

        ok, ex = utils.check_schema(data, 'bid-response')

        if not ok:
            raise ex


class BidAgentManager(object):

    def __init__(self, agents, timeout=0.5):

        logger.info('init bid-agent-manager (timeout=%fs)', timeout)
        self.timeout = timeout
        self.agents = [BidAgent(self, **i) for i in agents]

    def sendall(self, msg):

        logger.debug('send bid-request to %d dsps', len(self.agents))
        with ThreadPoolExecutor(max_workers=len(self.agents)) as exc:
            exc.map(lambda agent: agent.send(msg), self.agents)
        msg.freeze()


class BidNoticer(object):

    def __init__(self, timeout):

        self.timeout = timeout

    def sendall(self, params):

        with ThreadPoolExecutor(max_workers=len(params)) as exc:
            exc.map(lambda x: self.send(*x), params)

    def send(self, dsp, url, data):

        try:
            logger.debug('send bid-notice to: %s (%s)', dsp, 'win' if 'win' in data else 'lose')
            requests.post(url, json=data, timeout=self.timeout)
        except:
            pass


class BidEngine(object):

    def __init__(self, manager, noticer):

        logger.info('init bid-engine')
        self.manager = manager
        self.noticer = noticer
        self.stats = Stats()
        self.stats.set_value('started_time', time.time())

    def handle(self, req):

        self.stats.inc_value('bid_count')
        logger.info('handle request')
        msg = BidMessage.make(req)
        logger.debug('before: %s', msg)
        self.manager.sendall(msg)
        self.resolve(msg)
        logger.debug('after: %s', msg)
        self.notice(msg)
        self.stats.max_value('max_bid_time', msg.elapsed_time)
        self.stats.min_value('min_bid_time', msg.elapsed_time)
        return msg.get_response()

    def resolve(self, msg):

        try:
            results = msg.get_results()
            logger.debug('try to resolve %d results', len(results))
            Resolver.resolve(msg)
            logger.debug('resolution succeed')
        except:
            msg.set_empty_response()
            logger.debug('resolution failed')

    def notice(self, msg):

        results = msg.get_results()
        winners, losers = msg.get_decision()

        params = []

        for k, v in results.items():
            key = 'win' if k in winners else 'lose'
            dsp = k
            url = v['nurl']
            data = {'id': msg.uuid, key: {}}
            params.append((dsp, url, data))

        logger.debug('send bid-notice to %d dsps (win/lose)', len(results))
        self.noticer.sendall(params)


class Resolver(object):

    @staticmethod
    def resolve(msg):

        request = msg.get_request()
        results = msg.get_results()
        slots = []

        for k, v in results.items():
            for m in v['adm']:
                slot = {
                    'did': k,
                    'adm': m,
                }
                slots.append(slot)

        slots.sort(key=lambda x: x['adm']['price'], reverse=True)
        count = request['adunit']['param']['count']
        slots = slots[:count]

        players = set(results.keys())
        winners = set([i['did'] for i in slots])
        losers = players - winners

        result = {
            'adm': [dicttoolz.keyfilter(lambda x: x not in ['price'], i['adm']) for i in slots],
            'is_test': 0,
        }

        msg.set_decision(winners, losers)
        msg.set_response(result)

