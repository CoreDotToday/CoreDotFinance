from finance.statistics.basic.index import *
from finance.code_number import *
from finance.json_to_df import *


# statistics
def data_reader(code, start=None, end=None, day=None, division=None, bond=None, ind_name=None, stc_name=None):
    # assert f"{code}" in code_list, "Wrong code number"
    if code in index_code_list_stock:
        df = Stock(code, start, end, day, division, bond, ind_name, stc_name).read()
    elif code in index_code_list_bond:
        df = Bond(code, start, end, day, division, bond, ind_name, stc_name).read()
    return convert(df)



# visual
def data_visual():
    pass


# analysis
def data_analysis():
    pass