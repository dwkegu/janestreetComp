def strategy_simple(book, *arg, **kargs):
    return strategy_for_BOND(book["BOND"])


def strategy_for_BOND(book, *arg, **kwargs):
    if book is None:
        return None
    my_buy = None
    my_sell = None
    if book["sell"] is not None and len(book["sell"]) > 0:
        sorted_sell = sorted(book["sell"], key=lambda x: x[0])
        my_buy = sorted_sell[0]
    if book["sell"] is not None and len(book["buy"]) > 0:
        sorted_buy = sorted(book["buy"])
        my_sell = sorted_buy[-1]
    return {"buy": my_buy, "sell": my_sell}
