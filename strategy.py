def strategy_simple(priv_m, book, *arg, **kargs):
    return strategy_for_BOND(priv_m, book["BOND"])

def vwap(priv_m, book):
    if book is None:
        return None
    for item in book:
        pass


def strategy_for_BOND(priv_m, book, *arg, **kwargs):
    """

    :param priv_m:
    :param book:
    :param arg:
    :param kwargs:
    :return:
    """
    if book is None:
        return None
    my_buy = None
    my_sell = None
    if book["sell"] is not None and len(book["sell"]) > 0:
        sorted_sell = sorted(book["sell"], key=lambda x: x[0])
        my_buy = sorted_sell[0]
        my_buy[1] = min(my_buy[1], priv_m.limit_dict["bond"] - priv_m.bond)
    if book["sell"] is not None and len(book["buy"]) > 0:
        sorted_buy = sorted(book["buy"])
        my_sell = sorted_buy[-1]
        my_buy[1] = min(my_sell[1], priv_m.limit_dict["bond"] + priv_m.bond)
    return {"buy":{"BOND":my_buy,}, "sell":{"BOND":my_sell}}
