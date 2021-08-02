import json
import re
import warnings
import os

import pandas as pd

def get_shares_volume_column(columns):

    for shares_column in ['상장주식수', '상장좌수', "shares_outstanding"]:
        if shares_column in columns:
            shares = shares_column
            break
        else:
            shares = None

    for volume_column in ['거래량', 'volume']:
        if volume_column in columns:
            volume = volume_column
            break
        else:
            volume = None

    return shares, volume


def adjust_price(dataframe: pd.DataFrame):
    # column has to be Korean column name
    shares, volume = get_shares_volume_column(dataframe.columns)

    if shares is None or volume is None:
        warnings.warn("This data is not available to get adjusted price")
        return dataframe

    standard_ratio = dataframe[shares][0] / dataframe[shares]

    available_column_list = ["close", "change", "open", "high", "low", "volume", "종가", "대비", "시가", "고가", "저가", "거래량"]

    for column in available_column_list:
        data = dataframe.get(column)
        if data is None:
            continue
        if column == volume:
            # volume only needs to be multiplied by standard_ratio
            dataframe[column] = (data * standard_ratio).astype(int)
        else:
            dataframe[column] = (data / standard_ratio).astype(int)
    return dataframe


def is_kor_column(column_list: pd.DataFrame.index):
    reg = re.compile(r"[A-z]")
    for column in column_list:
        if not reg.match(column):
            return True
    return False


def get_column_map(file):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(BASE_DIR, f"{file}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def rename_dataframe(dataframe, column_file_name):
    new_column = get_column_map(column_file_name)
    return dataframe.rename(columns=new_column)


def options(dataframe, **kwargs):
    if not isinstance(dataframe, pd.DataFrame):
        return dataframe

    if kwargs.get("adjust") is True:
        dataframe = adjust_price(dataframe)

    if isinstance(dataframe.columns, pd.core.indexes.multi.MultiIndex):
        if kwargs.get("kor") is True:
            pass
        else:
            dataframe = rename_dataframe(dataframe, column_file_name='kor2eng')
    else:
        if kwargs.get("kor") is True:
            # dataframe is coming with Korean columns so when kor is None, then if has to be changed
            if not is_kor_column(dataframe.columns):
                dataframe = rename_dataframe(dataframe, column_file_name="eng2kor")
        else:
            if is_kor_column(dataframe.columns):
                dataframe = rename_dataframe(dataframe, column_file_name="kor2eng")

    if kwargs.get("reverse") is True:
        dataframe = dataframe.iloc[::-1]

    return dataframe
