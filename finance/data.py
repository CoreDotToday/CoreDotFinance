from finance.statistics.basic.index import StockIndex, BondIndex, DerivationIndex
from finance.statistics.basic import stock
from finance.statistics.basic.stock import OtherSecurity, Detail
from finance.statistics.basic.products import ELW, ETN, ETF
from finance.statistics.basic import bond
from finance.code_number import *
from finance.json_to_df import convert


# statistics
def data_reader(code, start=None, end=None, day=None,
                division=None, ind_name=None, stk_name=None,
                adj_price=False, investor=None, product=None,
                options=[], **kwargs):
    # assert f"{code}" in code_list, "Wrong code number"

    if code in index_code_list_stock:
        df, new_col_map = StockIndex(code, start, end, day, division, ind_name).read()
    elif code in index_code_list_bond:
        df, new_col_map = BondIndex(code, start, end, day, division).read()
    elif code in index_code_list_derivation:
        df, new_col_map = DerivationIndex(code, start, end, day, division, ind_name).read()

    elif code in stock_code_list_item:
        df, new_col_map = stock.ItemPrice(code, start, end, day, division, adj_price, stk_name).read()
    elif code in stock_code_list_info:
        df, new_col_map = stock.ItemInfo(code, start, end, day, division, stk_name).read()
    elif code in stock_code_list_trade:
        df, new_col_map = stock.TradePerform(code, start, end, day, division, stk_name, options, investor, **kwargs).read()
    elif code in stock_code_list_others:
        df, new_col_map = OtherSecurity(code, start, end, day, division, stk_name).read()
    elif code in stock_code_list_detail:
        df, new_col_map = Detail(code, start, end, day, division, stk_name, **kwargs).read()

    elif code in product_code_list_ETF:
        df, new_col_map = ETF(code, start, end, day, product, **kwargs).read()
    elif code in product_code_list_ETN:
        df, new_col_map = ETN(code, start, end, day, product, **kwargs).read()
    elif code in product_code_list_ELW:
        df, new_col_map = ELW(code, start, end, day, product, **kwargs).read()

    elif code in bond_code_list_price:
        df, new_col_map = bond.ItemPrice(code, start, end, day, product, **kwargs).read()
    elif code in bond_code_list_info:
        df, new_col_map = bond.ItemInfo(code, start, end, day, product, **kwargs).read()
    elif code in bond_code_list_trade:
        df, new_col_map = bond.TradePerform(code, start, end, day, product, **kwargs).read()
    elif code in bond_code_list_detail:
        df, new_col_map = bond.Detail(code, start, end, day, product, **kwargs).read()

    else:
        raise ValueError(f"No function code, [{code}]")
    return convert(df, new_col_map)


# visual
def data_visual():
    pass


# analysis
def data_analysis():
    pass