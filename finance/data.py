from finance.statistics.basic.index import *
from finance.statistics.basic.stock import *
from finance.code_number import *
from finance.json_to_df import *


# statistics
def data_reader(code, start=None, end=None, day=None,
                division=None, ind_name=None, stc_name=None,
                adj_price=False, inverstor=None, options=[], **kwargs):
    # assert f"{code}" in code_list, "Wrong code number"
    if code in index_code_list_stock:
        df = StockIndex(code, start, end, day, division, ind_name).read()
    elif code in index_code_list_bond:
        df = BondIndex(code, start, end, day, division).read()
    elif code in index_code_list_derivation:
        df = DerivationIndex(code, start, end, day, division, ind_name).read()
    elif code in stock_code_list_item:
        df = ItemPrice(code, start, end, day, division, adj_price, stc_name).read()
    elif code in stock_code_list_info:
        df = ItemInfo(code, start, end, day, division, stc_name).read()
    elif code in stock_code_list_trade:
        df = TradePerform(code, start, end, day, division, stc_name, options, inverstor, **kwargs).read()
    elif code in stock_code_list_others:
        df = OtherSecurity(code, start, end, day, division, stc_name).read()
    elif code in stock_code_list_detail:
        df = Detail(code, start, end, day, division, stc_name, **kwargs).read()

    return convert(df)



# visual
def data_visual():
    pass


# analysis
def data_analysis():
    pass