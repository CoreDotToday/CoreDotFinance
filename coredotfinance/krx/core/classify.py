from coredotfinance.krx.core.krx_website import stock
from coredotfinance.krx.core.krx_website import products
from coredotfinance.krx.core.krx_website import index
from coredotfinance.krx.core.function_code_list import *


def get_krx_instance(code, symbol, start, end, date, **kwargs):
    # Fixme : 지금은 stock, product만 추가되어 있다.
    #   index, commodity, bond, derivatice, oversees 등도 추가해주자.

    day = kwargs.get("day")
    division = kwargs.get("division")
    item = kwargs.get("item")

    if code in stock_code_list:
        krx_instance = stock.Stock(
            code, symbol=symbol, start=start, end=end, date=date, **kwargs
        )
    elif code in product_code_list:
        krx_instance = products.Product(
            code, symbol=symbol, start=start, end=end, date=date, **kwargs
        )
    elif code in index_code_list:
        krx_instance = index.Index(
            code, symbol=symbol, start=start, end=end, date=date, **kwargs
        )

    else:
        raise ValueError(f"No function code, [{code}]")

    return krx_instance
