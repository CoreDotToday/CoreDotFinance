# -*- coding: utf-8 -*-
import pandas as pd

from coredotfinance._krx.data_reader_ import data_reader


def stock(symbol="all", start=None, end=None):
    """
    Returns DataFrame of stock data in korean stock market from data.krx.co.kr.

    Parameters
    ----------
    symbol : str
        stands for stock symbol which is used to called in Korean stock market.
        Proper ticker is needed for each source.
    start : str
        stands for start date DataReader fetches data from.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"
    end : str
        stands for end date DataReader fetches data until.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"

    Returns
    --------
    Stock prices data in Kospi, Kosdaq, Konex : DataFrame
    """
    return data_reader("12003", symbol=symbol, start=start, end=end)


def per(symbol="all", start=None, end=None):
    """
    Returns DataFrame of price info data in korean stock market from data.krx.co.kr.

    Parameters
    ----------
    symbol : str
        stands for stock symbol which is used to called in Korean stock market.
        Proper ticker is needed for each source.
    start : str
        stands for start date DataReader fetches data from.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"
    end : str
        stands for end date DataReader fetches data until.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"

    Returns
    --------
    Stock prices data in Kospi, Kosdaq, Konex : DataFrame
    """
    return data_reader("12021", symbol=symbol, start=start, end=end, search_type="개별추이")


def etf(symbol="all", start=None, end=None):
    """
    Returns DataFrame of ETF data in korean stock market from data.krx.co.kr.

    Parameters
    ----------
    symbol : str
        stands for stock symbol which is used to called in Korean stock market.
        Proper ticker is needed for each source.
    start : str
        stands for start date DataReader fetches data from.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"
    end : str
        stands for end date DataReader fetches data until.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"

    Returns
    --------
    Stock prices data in Kospi, Kosdaq, Konex : DataFrame
    """
    return data_reader("13103", symbol=symbol, start=start, end=end)


def etn(symbol="all", start=None, end=None):
    """
    Returns DataFrame of ETN data in korean stock market from data.krx.co.kr.

    Parameters
    ----------
    symbol : str
        stands for stock symbol which is used to called in Korean stock market.
        Proper ticker is needed for each source.
    start : str
        stands for start date DataReader fetches data from.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"
    end : str
        stands for end date DataReader fetches data until.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"

    Returns
    --------
    Stock prices data in Kospi, Kosdaq, Konex : DataFrame
    """
    return data_reader("13203",  symbol=symbol, start=start, end=end)


def elw(symbol="all", start=None, end=None):
    """
    Returns DataFrame of ELW data in korean stock market from data.krx.co.kr.

    Parameters
    ----------
    symbol : str
        stands for stock symbol which is used to called in Korean stock market.
        Proper ticker is needed for each source.
    start : str
        stands for start date DataReader fetches data from.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"
    end : str
        stands for end date DataReader fetches data until.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"

    Returns
    --------
    Stock prices data in Kospi, Kosdaq, Konex : DataFrame
    """
    return data_reader('13302', symbol=symbol, start=start, end=end)


def bond(symbol="all", start=None, end=None):
    """
    Returns DataFrame of bond data in korean stock market from data.krx.co.kr.

    Parameters
    ----------
    symbol : str
        stands for stock symbol which is used to called in Korean stock market.
        Proper ticker is needed for each source.
    start : str
        stands for start date DataReader fetches data from.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"
    end : str
        stands for end date DataReader fetches data until.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"

    Returns
    --------
    Stock prices data in Kospi, Kosdaq, Konex : DataFrame
    """
    if symbol == "all":
        data1 = data_reader("14001", market="국채전문유통시장")
        data2 = data_reader("14001", market="일반채권시장")
        data3 = data_reader("14001", market="소액채권시장")
        return pd.concat([data1, data2, data3], ignore_index=True)
    else:
        pass
