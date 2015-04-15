#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    paxp2.bid
    ~~~~~~~~~
    This module implements the bidding logic
'''

import requests
import uuid


class BidRequest(object):

    @staticmethod
    def make(data):
        return BidRequest(data)

    def __init__(self, data):
        self.uuid = uuid.uuid4()
        self.data = data


class BidResponse(object):

    @staticmethod
    def make(data):
        return BidResponse()

    def __init__(self, data):
        self.data = data


class BidAgent(object):

    def __init__(self, id, name, burl):

        self.id = id
        self.name = name
        self.burl = burl

    def send(self, bid_request):

        print('send bid-request to:', self.id)


class BidAgentManager(object):

    def __init__(self, agents):

        self.agents = [BidAgent(**i) for i in agents]

    def sendall(self, bid_request):

        print('=== sending bid-request ===')
        for agent in self.agents:
            agent.send(bid_request)


class BidEngine(object):

    def __init__(self, manager):

        self.manager = manager

    def handle(self, req):

        bid_request = BidRequest.make(req)
        self.manager.sendall(bid_request)
        return {'id': 'helloworld'}

