from finance.statistics.basic.index import *
from finance.code_number import *
from finance.json_to_df import *


# statistics
def data_reader(code, start=None, end=None, division=None):
    assert f"{code}" in code_list, "Wrong code number"

    if code in index_code_list:
        df = Stock(code, start, end, division).read()
        return convert_key(df)


# visual
def data_visual():
    pass


# analysis
def data_analysis():
    pass