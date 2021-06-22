from coredotfinance.krx.krx_website.index import StockIndex, BondIndex, DerivationIndex
from coredotfinance.krx.krx_website import stock
from coredotfinance.krx.krx_website import products
from coredotfinance.krx.krx_website.commodity import Oil, Gold, CarbonEmission
from coredotfinance.krx.krx_website import bond, derivative, oversees
from coredotfinance.krx.function_code_list import *


def get_krx_instance(code, symbol, start, end, date, **kwargs):
    # Fixme : day, division 모두 kwargs 안으로 들어갈 것.
    #   두 파라미터 뿐만 아니라 다른 파라미터들도  kwargs 안에 넣을 것.

    day = kwargs.get('day')
    division = kwargs.get('division')
    item = kwargs.get('item')

    if code in stock_code_list:
        krx_instance = stock.Stock(code, symbol=symbol, start=start, end=end, date=date, **kwargs)
    elif code in product_code_list:
        krx_instance = products.Product(code, symbol=symbol, start=start, end=end, date=date, **kwargs)


    else:
        raise ValueError(f"No function code, [{code}]")

    return krx_instance
