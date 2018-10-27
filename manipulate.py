#!/usr/bin/python
from net_utils import ClientMessage
import json
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

    def buy(self, type, price, number):
        """
        :param type:
        :return: real buy number
        """
        number = min(number, self.limit(type)[0])
        self.name_dict[type] += number
        self.pnl -= price*number
        return number

    def sell(self, type, price, number):
        number = min(number, self.limit(type)[1])
        self.name_dict[type] -= number
        self.pnl += price*number
        return number


class Manipulate(PrivateBot):
    def __init__(self, alg, exchange):
        super(Manipulate, self).__init__()
        self.order_id = 0
        self.alg = alg
        self.exchange = exchange
        pass

    def add_operation(self, json):
        buy_dict, sell_dict = {}, {}
        for key in buy_dict:
            # no manipulation
            if buy_dict[key][1] == 0:
                continue
            # try add trade to the market bot
            self.write_to_exchange(self.exchange, ClientMessage.add(self.order_id, buy_dict[key][0], buy_dict[key][1], key))

            # if fill, add hold to the private bot
            if True:
                self.buy(key, price, fill_num)
        for key in sell_dict:
            if sell_dict[key][1] == 0:
                continue
            # try add trade to the market bot
            # function()
            # if fill, add hold to the private bot
            if True:
                self.sell(key, price, fill_num)

    @property
    def pnl(self):
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
