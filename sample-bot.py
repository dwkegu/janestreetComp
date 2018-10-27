#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
from datetime import datetime, timedelta
import random

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
from ServerMarket import ServerMessage
from manipulate import PrivateBot, Manipulate
from strategy import strategy_simple

team_name="Lotad"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=0
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())

def get_order_id():
    now = datetime.now().strftime("%Y%m%d%H%M")
    return now+random.randint(0, 100000)

def exchange_stock(exchange, strategy):
    cur_order = {}
    for item in strategy:
        cur_order[item] = {}
        for sto_item in strategy[item]:
            cur_order[item][sto_item] = {}
            t_id = get_order_id()
            cur_order[item][sto_item]["id"] = t_id
            cur_order[item][sto_item]["info"] = strategy[item][sto_item]
            write_to_exchange(exchange, {"type":"add", "symbol":item, "order_id": t_id, "dir":str(sto_item).upper(), "price": strategy[item][sto_item][0], "size": strategy[item][sto_item][1]})
    pass


# ~~~~~============== MAIN LOOP ==============~~~~~

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    td = timedelta(seconds=1)
    c = 0
    sm = ServerMessage(exchange)
    priv_msg = Manipulate(None, exchange)
    while c<10:
        c += 1
        books, trades, open, close = sm.get_current_book(4)
        print(books.keys())
        print(len(trades))
        my_stra = strategy_simple(priv_msg, books, trades)
        print(my_stra)
        if my_stra is None:
            continue
        else:
            priv_msg.trade_process(my_stra["buy"], my_stra["sell"], time_out=5)
            priv_msg.print_all()
            pass
    exchange.close()

def get_his():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    sm = ServerMessage(exchange)
    priv_msg = Manipulate(None, exchange)
    books, trades, open_, close = sm.get_current_book(100)
    trades = sm.get_history_trade()
    print(trades)
    stas ={}
    for trade in trades:
        for item in trade:
           if item in stas:
               stas[item].append(trade[item]["price"])
           else:
               stas[item] = [trade[item]["price"]]
    with open("/home/ubuntu/psfpy/stas.json", 'w', encoding="utf-8") as f:
        json.dump(stas, f)

if __name__ == "__main__":
    get_his()
