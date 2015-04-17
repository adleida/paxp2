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
from .stats import Stats


logger = logging.getLogger(__name__)


class BidMessage(object):

    @staticmethod
    def make(request_data):
        return BidMessage(request_data)

    def __init__(self, request_data):
        self.uuid = uuid.uuid4()
        self.request_data = request_data
        self.start_time = time.time()
        self.freezed = False
        self.results = {}

    def freeze(self):
        self.freezed = True

    def add_result(self, result):
        if not self.freezed:
            now = time.time()
            did = result['did']
            self.results[did] = result

    def get_results(self):
        return self.results

    def set_response(self, response_data):
        self.response_data = response_data
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

    def set_empty_response(self):
        empty_response_data = {'id': 'xxxx', 'data': 'no dsp response'}
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
            results:  {}
            ------------------
            start:    {}
            end:      {}
            elapsed:  {:.2f} ms
            ==================
            '''.format(self.uuid, self.request_data, self.response_data, self.results, self.start_time, self.end_time, self.elapsed_time*1000)
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
            self._check(result)
            msg.add_result(result)
            logger.debug('recv bid-response from: %s', self.id)
        except Exception as ex:
            logger.warning('cannot recv bid-response from: %s (%s)', self.id, ex)

    def _send(self, data):

        time.sleep(.5)
        return requests.post(self.burl, json=data, timeout=self.mgr.timeout).json()

    def _check(self, data):

        try:
            assert isinstance(data, dict)
            assert data.get('did') == self.id
        except:
            raise Exception('bad data')


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


class BidNotice(object):

    def sendall(self, msg):
        pass

    def send(self, nurl, win):
        pass


class BidEngine(object):

    def __init__(self, manager):

        logger.info('init bid-engine')
        self.manager = manager
        self.stats = Stats()
        self.stats.set_value('started_time', time.time())

    def handle(self, req):

        self.stats.inc_value('bid_count')
        logger.info('handle request')
        msg = BidMessage.make(req)
        logger.debug('before: %s', msg)
        self.manager.sendall(msg)
        self.resolve(msg)
        self.notice(msg)
        logger.debug('after: %s', msg)
        self.stats.max_value('max_bid_time', msg.elapsed_time)
        self.stats.min_value('min_bid_time', msg.elapsed_time)
        return msg.get_response()

    def resolve(self, msg):

        try:
            results = msg.get_results()
            logger.debug('try to resolve %d results', len(results))
            result = list(results.values())[0]
            result = self.cleanup(result)
            msg.set_response(result)
            logger.debug('resolution succeed')
        except:
            msg.set_empty_response()
            logger.debug('resolution failed')

    def cleanup(self, data):

        result = copy.deepcopy(data)
        result['did'] = 'adleida ad exchange'
        result['nurl'] = 'http://adx.adleida.com/v1/notice/'
        return result

    def notice(self, msg):

        logger.debug('send bid-notice to %d DSPs', len(msg.get_results()))

        response = msg.get_response()
        results = msg.get_results()

        for k, v in results:
            pass

