# -*- coding: utf-8 -*-
import pandas as pd

from finance.data_reader import data_reader
from finance import utils
from finance.log.log import Log


@Log.info
def get(stock="all", start=None, end=None):
    """
    코스피(KOSPI), 코스닥(KOSDAQ), 코넥스(KONEX)에 상장되어 있는 종목들에 대한 가격 데이터를 반환한다.
    Parameters
    ----------
    stock : string
        종목명 또는 종목코드를 입력. default 값은 "all"이며 전종목 시세를 반환한다.
    start : int, string
        검색 시작일, default 값은 오늘로부터 60일 이전
    end : int, string
        검색 종료일, default 값은 오늘

    Returns : DataFrame
    -------
    """
    utils.start_end_validation(start, end)
    if stock == "all":
        return data_reader("12001", market="전체", day=start)
    else:
        if utils.classifier(stock) == "item code":
            return data_reader("12003", start=start, end=end, item_code=stock)
        else:
            return data_reader("12003", start=start, end=end, item=stock)


@Log.info
def per(stock="all", start=None, end=None):
    """
    코스피(KOSPI), 코스닥(KOSDAQ), 코넥스(KONEX)에 상장되어 있는 종목들에 대한
    PER/EPS/PBS/BPS/주당배당금/배당수익률 데이터를 반환한다.
    Parameters
    ----------
    stock : string
        종목명 또는 종목코드를 입력. default 값은 "all"이며 전종목 시세를 반환한다.
    start : int, string
        검색 시작일, default 값은 오늘로부터 60일 이전
    end : int, string
        검색 종료일, default 값은 오늘

    Returns : DataFrame
    -------
    """
    utils.start_end_validation(start, end)
    if stock == "all":
        data = data_reader("12021", search_type="전종목", market="전체", day=start)
        #  12021 종목명 데이터에 아래와 같은 문자열이 함께 출력됨.
        data["종목명"] = [name.replace("<em class =\"up\"></em>", "") for name in data["종목명"]]
        return data
    else:
        if utils.classifier(stock) == "item code":
            return data_reader("12021", search_type="개별추이", item_code=stock, start=start, end=end)
        else:
            return data_reader("12021", search_type="개별추이", item=stock, start=start, end=end)


@Log.info
def etf(item="all", start=None, end=None):
    """
    Parameters
    ----------
    item : string
        ETF 종목명 또는 ETF 종목코드를 입력. default 값은 "all"이며 전종목 시세를 반환한다.
    start : int, string
        검색 시작일, default 값은 오늘로부터 60일 이전
    end : int, string
        검색 종료일, default 값은 오늘

    Returns : DataFrame
    -------
    """
    utils.start_end_validation(start, end)
    if item == "all":
        return data_reader("13101")
    else:
        if utils.classifier(item) == "item code":
            return data_reader("13103", item_code=item, start=start, end=end)
        else:
            return data_reader("13103", item=item, start=start, end=end)


@Log.info
def etn(item="all", start=None, end=None):
    """
    Parameters
    ----------
    item : string
        ETN 종목명 또는 ETN 종목코드를 입력. default 값은 "all"이며 전종목 시세를 반환한다.
    start : int, string
        검색 시작일, default 값은 오늘로부터 60일 이전
    end : int, string
        검색 종료일, default 값은 오늘

    Returns : DataFrame
    -------
    """
    utils.start_end_validation(start, end)
    if item == "all":
        return data_reader("13201")
    else:
        if utils.classifier(item) == "item code":
            return data_reader("13203", item_code=item, start=start, end=end)
        else:
            return data_reader("13203", item=item, start=start, end=end)


@Log.info
def elw(item="all", start=None, end=None):
    """
    Parameters
    ----------
    item : string
        ELW 종목명 또는 ELW 종목코드를 입력. default 값은 "all"이며 전종목 시세를 반환한다.
    start : int, string
        검색 시작일, default 값은 오늘로부터 60일 이전
    end : int, string
        검색 종료일, default 값은 오늘

    Returns : DataFrame
    -------
    """
    utils.start_end_validation(start, end)
    if item == "all":
        return data_reader("13301")
    else:
        if utils.classifier(item, "elw") == "item code":
            return data_reader("13302", item_code=item, start=start, end=end)
        else:
            return data_reader("13302", item=item, start=start, end=end)


@Log.info
def bond(item="all", start=None, end=None):
    """
    Parameters
    ----------
    item : string
        채권 종목명 또는 채권 종목코드를 입력. default 값은 "all"이며 국채전문유통시장, 일반채권시장, 소액채권시장의 종목들을 모두 보여준다.
    start : int, string
        검색 시작일, default 값은 오늘로부터 60일 이전
    end : int, string
        검색 종료일, default 값은 오늘

    Returns : DataFrame
    -------
    """
    utils.start_end_validation(start, end)
    if item == "all":
        data1 = data_reader('14001', market='국채전문유통시장')
        data2 = data_reader('14001', market='일반채권시장')
        data3 = data_reader('14001', market='소액채권시장')
        return pd.concat([data1, data2, data3], ignore_index=True)
    else:
        pass

