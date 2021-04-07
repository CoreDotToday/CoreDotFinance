# -*- coding: utf-8 -*-
import re
from finance.data_reader import data_reader

stock_code_list = data_reader('12021', market='전체', search_type='전종목')['종목코드'].array


def get(stock='all', start=None, end=None):
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
    if stock == 'all':
        return data_reader('12001', market='전체', day=start)
    else:
        if stock in stock_code_list:
            return data_reader('12003', start=start, end=end, item_code=stock)
        else:
            return data_reader('12003', start=start, end=end, item=stock)


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
    if stock == 'all':
        data = data_reader('12021', search_type='전종목', market='전체', day=start)
        #  12021 종목명 데이터에 아래와 같은 문자열이 함께 출력됨.
        data['종목명'] = [name.replace('<em class =\"up\"></em>', '') for name in data['종목명']]
        return data
    else:
        if stock in stock_code_list:
            return data_reader('12021', search_type='개별추이', item_code=stock, start=start, end=end)
        else:
            return data_reader('12021', search_type='개별추이', item=stock, start=start, end=end)


def etf(item="all", start=None, end=None):
    """
    Parameters
    ----------
    item
    start
    end

    Returns
    -------

    """
