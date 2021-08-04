# -*- coding: utf-8 -*-
import os

from coredotfinance.krx.core.process import get_dataframe
from coredotfinance.krx.core.classify import get_krx_instance
from coredotfinance.krx.core import fetch, column
from coredotfinance.krx.core import jsp_util

"""
data_reader는 data.krx.co.kr로 부터 데이터를 가져온다.
불러온 데이터는 Json 형태이며 key 값은 영문약자로 되어 있다.
영문약자를 한글로 바꾸어 주기위해 data.krx.co.kr에서 .jsp 퍄일을 가져온다.
.jsp 파일의 url을 얻기위해서는 'MDCSTAT' 으로 시작하는 쿼리 단어를 얻어야 하고
그 단어는 post_params의 'bld' 값에 들어 있다.
"""


def data_reader(code, symbol=None, start=None, end=None, date=None, **kwargs):
    """
    data.krx.co.kr 에서 데이터를 읽어 온다.

    Parameters
    ----------
    code : str
        수행하고자 하는 krx의 기능번호.
        https://data.krx.co.kr에서 이용하고자 하는 기능에 이용번호를 입력한다.
    symbol : str, int
        조회하고자 하는 데이터의 종목코드.
        형태는 종목과 종류마다 다르다. 예) 삼성전자 : '005930', ARIRANG 200 : '152100'
    start : str
        조회하고자 하는 데이터의 시작일.
        형태는 YYYYMMDD가 되어야 한다. 예) 20210601
    end : str
        조회하고자 하는 데이터의 종료일.
        형태는 YYYYMMDD가 되어야 한다. 예) 20210601
    date : str
        조회하고자 하는 데이터의 조회일.
        형태는 YYYYMMDD가 되어야 한다. 예) 20210601
    kwargs :
        kind : str
            조회하고자 하는 데이터의 종류
            krx : ['stock', 'etf', 'index' ,'per', 'index', 'other_index']
        division : str
            조회하고자 하는 데이터의 세부 구분
            other_index : ['선물지수', '옵션지수', '전략지수', '상품지수']


    Examples
    --------
    >>> from coredotfinance.krx.api.data_reader import data_reader
    >>> data_reader('11012', symbol='미국달러선물', start=20210101, end=20210701, kind='other_index', division='선물지수')


    Warnings
    --------
    시작일, 종료일, 조회일이 공휴일일 경우에는 해당일의 데이터가 없다.
    즉, data_reader("12003", symbol=symbol, start='202106019', end='20210620', kind=kind)을 호출하면 에러가 뜬다.


    Returns
    -------
    pd.DataFrame
    """

    if not isinstance(code, str):
        raise ValueError(f"code has to be {str} but got {type(code)}")
    krx_instance = get_krx_instance(
        code, symbol=symbol, start=start, end=end, date=date, **kwargs
    )
    post_params = krx_instance.get_requested_data()
    if symbol:
        symbol_name = krx_instance.data_nm
        print(symbol_name)

    mdcstat = _parse_mdcstat(post_params)
    jsp_soup = jsp_util.get_jsp_soup(mdcstat)
    valid_post_params = fetch.convert_vaild_post_params(jsp_soup, post_params)
    krx_data = fetch.get_krx_data(valid_post_params)
    korean_columns = column.get_korean_columns(jsp_soup, mdcstat)
    dataframe = get_dataframe(krx_data, korean_columns)

    return dataframe


def _parse_mdcstat(post_params):
    """
    parses mdcstat from bld in post_params.

    Parameters
    ----------
    post_params: dict

    Examples :
        {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01701",
            "tboxisuCd_finder_stkisu0_2": "060310/3S",
            "isuCd": "KR7060310000",
            "isuCd2": "060310",
            "codeNmisuCd_finder_stkisu0_2": "3S",
            "param1isuCd_finder_stkisu0_2": "STK",
            "strtDd": "000040",
            "endDd": "20210401",
            "MIME Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "csvxls_isNo": "false",
        }

    Returns
    -------
    In this case, MDCSTAT01701 will be returned
    """

    bld = post_params["bld"]
    mdcstat = bld.split("/")[-1]
    return mdcstat
