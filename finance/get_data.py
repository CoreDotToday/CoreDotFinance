from finance.statistics.basic.index import StockIndex, BondIndex, DerivationIndex
from finance.statistics.basic import stock
from finance.statistics.basic.stock import OtherSecurity, Detail
from finance.statistics.basic.products import ELW, ETN, ETF
from finance.statistics.basic.commodity import Oil, Gold, CarbonEmission
from finance.statistics.basic import bond, derivative, oversees
from finance.function_code_list import *


def get_data_json_and_column_map(code, start, end, day, division, item, **kwargs):
    # FIXME : Change the name of this function
    #  It is not that good
    if code in index_code_list_stock:
        data_json, column_map = StockIndex(code, start, end, day, division, item, **kwargs).function()
    elif code in index_code_list_bond:
        data_json, column_map = BondIndex(code, start, end, day, division).function()
    elif code in index_code_list_derivation:
        data_json, column_map = DerivationIndex(code, start, end, day, division, item).function()

    elif code in stock_code_list_item:
        data_json, column_map = stock.ItemPrice(code, start, end, day, division, item, **kwargs).function()
    elif code in stock_code_list_info:
        data_json, column_map = stock.ItemInfo(code, start, end, day, division).function()
    elif code in stock_code_list_trade:
        data_json, column_map = stock.TradePerform(code, start, end, day, division, item, **kwargs).function()
    elif code in stock_code_list_others:
        data_json, column_map = OtherSecurity(code, start, end, day, division).function()
    elif code in stock_code_list_detail:
        data_json, column_map = Detail(code, start, end, day, division, item, **kwargs).function()

    elif code in product_code_list_ETF:
        data_json, column_map = ETF(code, start, end, day, item, **kwargs).function()
    elif code in product_code_list_ETN:
        data_json, column_map = ETN(code, start, end, day, item, **kwargs).function()
    elif code in product_code_list_ELW:
        data_json, column_map = ELW(code, start, end, day, item, **kwargs).function()

    elif code in bond_code_list_price:
        data_json, column_map = bond.ItemPrice(code, start, end, day, item, **kwargs).function()
    elif code in bond_code_list_info:
        data_json, column_map = bond.ItemInfo(code, start, end, day, item, **kwargs).function()
    elif code in bond_code_list_trade:
        data_json, column_map = bond.TradePerform(code, start, end, day, item, **kwargs).function()
    elif code in bond_code_list_detail:
        data_json, column_map = bond.Detail(code, start, end, day, item, **kwargs).function()

    elif code in derivative_code_list_price:
        data_json, column_map = derivative.ItemPrice(code, start, end, day, item, **kwargs).function()
    elif code in derivative_code_list_info:
        data_json, column_map = derivative.ItemInfo(code, start, end, day, item, **kwargs).function()
    elif code in derivative_code_list_trade:
        data_json, column_map = derivative.TradePerform(code, start, end, day, item, **kwargs).function()
    elif code in derivative_code_list_detail:
        data_json, column_map = derivative.Detail(code, start, end, day, item, **kwargs).function()

    elif code in commodity_code_list_oil:
        data_json, column_map = Oil(code, start, end, day, **kwargs).function()
    elif code in commodity_code_list_gold:
        data_json, column_map = Gold(code, start, end, day, **kwargs).function()
    elif code in commodity_code_list_carbonemission:
        data_json, column_map = CarbonEmission(code, start, end, day, **kwargs).function()

    elif code in oversees_code_list_euro:
        data_json, column_map = oversees.EUREX(code, start, end, day, **kwargs).function()

    else:
        raise ValueError(f"No function code, [{code}]")

    return data_json, column_map
