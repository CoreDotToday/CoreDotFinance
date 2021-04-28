from finance.dataframing import to_dataframe
from finance.get_data import get_data_json_and_column_map


# statistics
def data_reader(code, start=None, end=None, day=None, division=None,  item=None, **kwargs):
    data_json, column_map = get_data_json_and_column_map(code, start, end, day, division, item, **kwargs)
    return to_dataframe(data_json, column_map)


# visual
def data_visual():
    pass


# analysis
def data_analysis():
    pass