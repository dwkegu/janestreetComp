def strategy_simple(priv_m, book, trades, *arg, **kargs):
    fair_price = vwap(trades)
    print('fair price is:', fair_price)
    if "BOND" in fair_price and 'BOND' in book:
        return strategy_for_BOND(priv_m, book["BOND"], fair_price["BOND"])
    else:
        return None

def vwap(trades):
    if trades is None:
        return None
    fair_price = {}
    s = {}
    s_size = {}
    for item in trades:

        list_item = item
        for item2 in list_item:
            s_ = list_item[item2]['price'] * list_item[item2]['size']
            if item2 in s:
                s[item2] += s_
                s_size[item2] += list_item[item2]['size']
            else:
                s[item2] = s_
                s_size[item2] = list_item[item2]['size']
    for item in s:
        fair_price[item] = s[item]/s_size[item]
    return fair_price

def strategy_for_BOND(priv_m, book, fair_price, *args, **kwargs):
    """

    :param priv_m:
    :param book:
    :param arg:
    :param kwargs:
    :return:
    """
    if book is None:
        return None
    my_buy = []
    my_sell = []
    if book["sell"] is not None and len(book["sell"]) > 0:
        sorted_sell = sorted(book["sell"], key=lambda x: x[0])
        for item in sorted_sell:
            if item[0] < fair_price:
                item[1] = min(item[1], priv_m.limit_dict["bond"] - priv_m.bond)
                my_buy.append(item)
    if book["buy"] is not None and len(book["buy"]) > 0:
        sorted_sell = sorted(book["buy"], key=lambda x: x[0])
        for item in sorted_sell:
            if item[0] > fair_price:
                item[1] = min(item[1], priv_m.limit_dict["bond"] - priv_m.bond)
                my_sell.append(item)
    return {"buy":{"BOND":my_buy,}, "sell":{"BOND":my_sell}}
