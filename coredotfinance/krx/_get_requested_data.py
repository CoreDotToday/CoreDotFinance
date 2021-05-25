from coredotfinance.krx.krx_website.index import StockIndex, BondIndex, DerivationIndex
from coredotfinance.krx.krx_website import stock
from coredotfinance.krx.krx_website.stock import OtherSecurity, Detail
from coredotfinance.krx.krx_website.products import ELW, ETN, ETF
from coredotfinance.krx.krx_website.commodity import Oil, Gold, CarbonEmission
from coredotfinance.krx.krx_website import bond, derivative, oversees
from coredotfinance.krx._function_code_list import *


def get_requested_data(code, start, end, day, division, item, **kwargs):
    # FIXME : Change the name of this function
    #  It is not that good
    if code in index_code_list_stock:
        requested_data = StockIndex(
            code, start, end, day, division, item, **kwargs
        ).get_requested_data()
    elif code in index_code_list_bond:
        requested_data = BondIndex(code, start, end, day, division).get_requested_data()
    elif code in index_code_list_derivation:
        requested_data = DerivationIndex(
            code, start, end, day, division, item
        ).get_requested_data()

    elif code in stock_code_list_item:
        requested_data = stock.ItemPrice(
            code, start, end, day, division, item, **kwargs
        ).get_requested_data()
    elif code in stock_code_list_info:
        requested_data = stock.ItemInfo(
            code, start, end, day, division
        ).get_requested_data()
    elif code in stock_code_list_trade:
        requested_data = stock.TradePerform(
            code, start, end, day, division, item, **kwargs
        ).get_requested_data()
    elif code in stock_code_list_others:
        requested_data = OtherSecurity(
            code, start, end, day, division
        ).get_requested_data()
    elif code in stock_code_list_detail:
        requested_data = Detail(
            code, start, end, day, division, item, **kwargs
        ).get_requested_data()

    elif code in product_code_list_ETF:
        requested_data = ETF(code, start, end, day, item, **kwargs).get_requested_data()
    elif code in product_code_list_ETN:
        requested_data = ETN(code, start, end, day, item, **kwargs).get_requested_data()
    elif code in product_code_list_ELW:
        requested_data = ELW(code, start, end, day, item, **kwargs).get_requested_data()

    elif code in bond_code_list_price:
        requested_data = bond.ItemPrice(
            code, start, end, day, item, **kwargs
        ).get_requested_data()
    elif code in bond_code_list_info:
        requested_data = bond.ItemInfo(
            code, start, end, day, item, **kwargs
        ).get_requested_data()
    elif code in bond_code_list_trade:
        requested_data = bond.TradePerform(
            code, start, end, day, item, **kwargs
        ).get_requested_data()
    elif code in bond_code_list_detail:
        requested_data = bond.Detail(
            code, start, end, day, item, **kwargs
        ).get_requested_data()

    elif code in derivative_code_list_price:
        requested_data = derivative.ItemPrice(
            code, start, end, day, item, **kwargs
        ).get_requested_data()
    elif code in derivative_code_list_info:
        requested_data = derivative.ItemInfo(
            code, start, end, day, item, **kwargs
        ).get_requested_data()
    elif code in derivative_code_list_trade:
        requested_data = derivative.TradePerform(
            code, start, end, day, item, **kwargs
        ).get_requested_data()
    elif code in derivative_code_list_detail:
        requested_data = derivative.Detail(
            code, start, end, day, item, **kwargs
        ).get_requested_data()

    elif code in commodity_code_list_oil:
        requested_data = Oil(code, start, end, day, **kwargs).get_requested_data()
    elif code in commodity_code_list_gold:
        requested_data = Gold(code, start, end, day, **kwargs).get_requested_data()
    elif code in commodity_code_list_carbonemission:
        requested_data = CarbonEmission(
            code, start, end, day, **kwargs
        ).get_requested_data()

    elif code in oversees_code_list_euro:
        requested_data = oversees.EUREX(
            code, start, end, day, **kwargs
        ).get_requested_data()

    else:
        raise ValueError(f"No function code, [{code}]")

    return requested_data
