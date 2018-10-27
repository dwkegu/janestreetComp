




class ClientMessage:
    def __init__(self):
        pass
    @staticmethod
    def hello():
        return {'type': 'hello', 'team': 'LATOD'}

    @staticmethod
    def add(order_id, price, size, symbol, op='buy'):
        if op == 'buy':
            return {'type': 'add', 'order_id': order_id, 'symbol': symbol.upper(), 'dir': 'BUY', 'price': price, 'size': size}
        elif op == 'sell':
            return {'type': 'add', 'order_id': order_id, 'symbol': symbol.upper(), 'dir': 'SELL', 'price': price, 'size': size}
        else:
            raise ValueError('add operation error: must be buy or sell')

    @staticmethod
    def convert(order_id, size, symbol, op='buy'):
        if op == 'buy':
            return {"type": "convert", "order_id": order_id, "symbol": symbol.upper(), "dir": "BUY", "size": size}
        elif op == 'sell':
            return {"type": "convert", "order_id": order_id, "symbol": symbol.upper(), "dir": "SELL", "size": size}
        else:
            raise ValueError('convert operation error: must be buy or sell')

    @staticmethod
    def cancel(order_id):
        return {"type": "cancel", "order_id": order_id}

