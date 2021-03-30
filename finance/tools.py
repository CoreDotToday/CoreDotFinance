# -*- coding: utf-8 -*-
import re

from finance.data_reader import data_reader

stock_code_list = data_reader('12021', market='전체', search_type='전종목')['종목코드'].array


def get(stock='all', start=None, end=None):
    """
    :param stock: 종목명 또는 종목코드, 기본값은 'all'
        'all' 은 전종목 시세
    :param start: 시작일 또는 조회일자
        검색 시작일 또는 조회일자
    :param end: 종료일
        검색 종료일
    :return: DataFrame or None
    """
    if stock == 'all':
        return data_reader('12001', market='전체', day=start)
    else:
        if stock in stock_code_list:
            return data_reader('12003', start=start, end=end, item_code=stock)
        else:
            return data_reader('12003', start=start, end=end, item=stock)


def per(stock='all', start=None, end=None):
    """
    :param stock: 종목명 또는 종목코드, 기본값은 'all'
        'all' 은 전종목 검색
    :param start: 시작일 또는 조회일자
        검색 시작일
    :param end: 종료일
        검색 종료
    :return: DataFrame or None
    """
    if stock == 'all':
        return data_reader('12021', search_type='전종목', market='전체', day=start)
    else:
        if stock in stock_code_list:
            return data_reader('12021', search_type='개별추이', item_code=stock, day=start)
        else:
            return data_reader('12021', search_type='개별추이', item=stock, day=start)