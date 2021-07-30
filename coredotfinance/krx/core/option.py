import json
import re
import warnings
import os

import pandas as pd

from coredotfinance.krx.core import column


def is_adjustable_Korean_column(columns):
    if "상장주식수" in columns:
        return True
    else:
        return False


def is_adjustable_English_column(columns):
    if "shares_outstanding" in columns:
        return True
    else:
        return False


def adjust_price(dataframe: pd.DataFrame):
    # column has to be Korean column name
    if is_adjustable_Korean_column(dataframe.columns):
        shares = "상장주식수"
        volume = "거래량"
        available_column_list = ["종가", "대비", "시가", "고가", "저가", "거래량"]
    elif is_adjustable_English_column(dataframe.columns):
        shares = "shares_outstanding"
        volume = "volume"
        available_column_list = ["close", "change", "open", "high", "low", "volume"]
    else:
        warnings.warn("This data is not available to get adjusted price")
        return dataframe

    standard_ratio = dataframe[shares][0] / dataframe[shares]
    for column in available_column_list:
        data = dataframe.get(column, None)
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


def options(dataframe, **kwargs):

    if kwargs.get("adjust", None) is True:
        dataframe = adjust_price(dataframe)

    if kwargs.get("kor", None) is True:
        # dataframe is coming with Korean columns so when kor is None, then if has to be changed
        if not is_kor_column(dataframe.columns):
            column_file_name = "eng2kor"
            english_column = get_column_map(column_file_name)
            dataframe.rename(columns=english_column, inplace=True)
    else:
        if is_kor_column(dataframe.columns):
            column_file_name = "kor2eng"
            korean_column = get_column_map(column_file_name)
            dataframe.rename(columns=korean_column, inplace=True)

    if kwargs.get("reverse", None) is True:
        dataframe = dataframe.iloc[::-1]

    return dataframe
