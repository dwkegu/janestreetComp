#!/usr/bin/python
from net_utils import ClientMessage
import json
import time
class PrivateBot:
    def __init__(self):
        self.bond = 0
        self.nike = 0
        self.adid = 0
        self.fyue = 0
        self.shoe = 0
        self.baba = 0
        self.baaz = 0
        self.stock = [self.nike, self.adid, self.fyue, self.baba]
        self.limit_dict = {'bond':100, 'nike':100, 'adid':100, 'fyue':100, 'shoe':100, 'baba':10, 'baaz':10}
        self.name_dict = {'bond': self.bond, 'nike': self.nike, 'adid': self.adid,
                          'fyue': self.fyue, 'shoe': self.shoe, 'baba': self.baba, 'baaz': self.baaz}
        self.pnl = 0

    def limit(self, type):
        """
        return the limit of buy and sell for each trade type
        :param self: trade type
        :return: buy_limit and sell_limit
        """
        if type not in self.limit_dict:
            raise ValueError('error trade type')
        buy_limit = self.limit_dict[type] - self.name_dict[type]
        sell_limit = self.limit_dict[type] + self.name_dict[type]
        return buy_limit, sell_limit

    def buy(self, stock, price, number):
        """
        :param type:
        :return: real buy number
        """
        number = min(number, self.limit(stock)[0])
        self.name_dict[stock] += number
        self.pnl -= price*number
        return number

    def sell(self, stock, price, number):
        number = min(number, self.limit(stock)[1])
        self.name_dict[stock] -= number
        self.pnl += price*number
        return number
    def print_all(self):
        print('bond', self.bond)
        print('nike', self.nike)
        print('adid', self.adid)
        print('fyue', self.fyue)
        print('shoe', self.shoe)
        print('baba', self.baba)
        print('baaz', self.baaz)

class Manipulate(PrivateBot):
    def __init__(self, alg, exchange):
        super(Manipulate, self).__init__()
        self.order_id = 0
        self.alg = alg
        self.exchange = exchange
        self.trade_dict = {}
        pass

    def add_operation(self, buy_dict, sell_dict, time_out=2):
        # buy_dict, sell_dict = {}, {}
        for key in buy_dict:
            # no manipulation
            if buy_dict[key][1] == 0:
                continue
            # try add trade to the market bot
            self.write_to_exchange(self.exchange, ClientMessage.add(self.order_id, buy_dict[key][0],
                                                                    buy_dict[key][1], key, op='buy'))
            self.trade_dict[self.order_id] = ('buy', key, buy_dict[key][0], buy_dict[key][1])
            self.order_id = (self.order_id + 1) % 1000000
            message = self.read_from_exchange(self.exchange)
            self._process_message(message)

        for key in sell_dict:
            if sell_dict[key][1] == 0:
                continue
            self.write_to_exchange(self.exchange,
                                   ClientMessage.add(self.order_id, sell_dict[key][0],
                                                     sell_dict[key][1], key, op='sell'))
            self.trade_dict[self.order_id] = ('sell', key, buy_dict[key][0], buy_dict[key][1])
            self.order_id = (self.order_id + 1) % 1000000
            message = self.read_from_exchange(self.exchange)
            self._process_message(message)
        spend = 0
        start_time = time.time()
        while spend < time_out:
            message = self.read_from_exchange(self.exchange)
            self._process_message(message)
            spend = time.time()-start_time

    def cancel_all_operation(self):
        for key in self.trade_dict:
            self.write_to_exchange(self.exchange, ClientMessage.cancel(key))
            message = self.read_from_exchange(self.exchange)
            self._process_message(message)
        while len(self.trade_dict):
            message = self.read_from_exchange(self.exchange)
            self._process_message(message)

    def trade_process(self, buy_dict, sell_dict, time_out=2):
        self.add_operation(buy_dict, sell_dict, time_out)
        self.cancel_all_operation()
        # achieve book
        # algorithm

    @property
    def pnl_real(self):
        """
        calculate the pnl in current state
        :return:
        """
        pnl = self.pnl
        # add price*number for each trade type
        # pnl += self.bond * bond_price
        # pnl += self.nike * nike_price
        # pnl += self.adid * adid_price
        # pnl += self.fyue * fyue_price
        # pnl += self.shoe * shoe_price
        # pnl += self.baba * baba_price
        # pnl += self.baaz * baaz_price
        return pnl

    @staticmethod
    def write_to_exchange(exchange, obj):
        json.dump(obj, exchange)
        exchange.write("\n")

    @staticmethod
    def read_from_exchange(exchange):
        return json.loads(exchange.readline())

    def _process_message(self, message):
        if message['type'] in ['book', 'open', 'close', 'trade', 'ack']:
            return
        elif message['type'] == 'reject':
            del self.trade_dict[message['order_id']]
        elif message['type'] == 'error':
            print(message)
            raise ValueError('message error')
        elif message['type'] == 'fill':
            order_id = message['order_id']
            trade_type, stock, price, size = self.trade_dict[order_id]
            if trade_type == 'buy':
                buy_size = self.buy(self.name_dict[stock], message['price'], message['size'])
                if size - buy_size == 0:
                    del self.trade_dict[order_id]
                else:
                    self.trade_dict[order_id] = (trade_type, stock, price, size-buy_size)
            elif trade_type == 'sell':
                sell_size = self.sell(self.name_dict[stock], message['price'], message['size'])
                if size - sell_size == 0:
                    del self.trade_dict[order_id]
                else:
                    self.trade_dict[order_id] = (trade_type, stock, price, size-sell_size)
            else:
                raise ValueError('trade error')
        elif message['type'] == 'out':
            order_id = message['order_id']
            try:
                del self.trade_dict[order_id]
            except:
                pass
        else:
            raise ValueError('error message type', message['type'])
