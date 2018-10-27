#!/usr/bin/python
# from net_utils import ClientMessage
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
