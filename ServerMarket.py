#!/usr/bin/env
# coding:utf-8
"""
Created on 18/10/27 上午11:28

base Info
"""
__author__ = 'xiaochenwang94'
__version__ = '1.0'

import os
import socket
import json
import time

team_name="Lotad"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=1
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname


class ServerMessage(object):
    def __init__(self, exchange):
        self.total_trade = []
        self.exchage = exchange

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((exchange_hostname, port))
        return s.makefile('rw', 1)

    def write_to_exchange(self, exchange, obj):
        json.dump(obj, exchange)
        exchange.write("\n")

    def read_from_exchange(self, exchange):
        return json.loads(exchange.readline())

    def get_current_book(self, time_delta):
        exchange = self.exchage
        self.write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
        t_s = time.time()
        result = []
        while time.time() - t_s < time_delta:
            # print(time.time() - t_s)
            hello_from_exchange = self.read_from_exchange(exchange)
            # print(hello_from_exchange)
            result.append(hello_from_exchange)
        ret = {}
        trades = {}
        opens = []
        closes = []
        for r in result:
            if r['type'] == 'book':
                ret[r['symbol']] = {
                     'buy': r['buy'],
                     'sell': r['sell']
                }
            if r['type'] == 'trade':
                trades[r['symbol']] = {
                    'price': r['price'],
                    'size': r['size']
                }
            if r['type'] == 'open':
                opens = r['symbols']
            if r['type'] == 'close':
                closes = r['symbols']
            self.total_trade.append(trades)
        return ret, trades, opens, closes

    def get_history_trade(self):
        return self.total_trade

if __name__ == '__main__':
    m = ServerMessage()
    print(m.get_current_book(1))
