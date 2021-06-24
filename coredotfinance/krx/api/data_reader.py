# -*- coding: utf-8 -*-
import os

from coredotfinance.krx.core.process import get_dataframe
from coredotfinance.krx.core.classify import get_krx_instance
from coredotfinance.krx.core import fetch, webio, column

"""
data_reader는 data.krx.co.kr로 부터 데이터를 가져온다.
불러온 데이터는 Json 형태이며 key 값은 영문약자로 되어 있다.
영문약자를 한글로 바꾸어 주기위해 data.krx.co.kr에서 .jsp 퍄일을 가져온다.
.jsp 파일의 url을 얻기위해서는 'MDCSTAT' 으로 시작하는 쿼리 단어를 얻어야 하고
그 단어는 post_params의 'bld' 값에 들어 있다.
"""


def data_reader(
    code, symbol=None, start=None, end=None, date=None, **kwargs
):
    """
    data.krx.co.kr 에서 데이터를 읽어 온다.

    Parameters
    ----------
    code : str
        수행하고자 하는 krx의 기능번호
        https://data.krx.co.kr에서 이용하고자 하는 기능에 이용번호를 입력한다.
    symbol : str
        조회하고자 하는 데이터의 종목코드
        형태는 종목과 종류마다 다르다. 예) 삼성전자 : '005930', ARIRANG 200 : '152100'
    start : str
        조회하고자 하는 데이터의 시작일
        형태는 YYYYMMDD가 되어야 한다. 예) 20210601
    end : str
        조회하고자 하는 데이터의 종료일
        형태는 YYYYMMDD가 되어야 한다. 예) 20210601
    date : str
        조회하고자 하는 데이터의 조회일
        형태는 YYYYMMDD가 되어야 한다. 예) 20210601

    Warnings
    --------
    시작일, 종료일, 조회일이 공휴일일 경우에는 해당일의 데이터가 없다.
    예) data_reader("12003", symbol=symbol, start='202106019', end='20210620', kind=kind)을 호출하면 에러가 뜬다.


    Returns
    -------

    """
    krx_instance = get_krx_instance(code, symbol=symbol, start=start, end=end, date=date, **kwargs)
    post_params = krx_instance.get_requested_data()
    if symbol:
        symbol_name = krx_instance.data_nm
        print(symbol_name)

    mdcstat = _parse_mdcstat(post_params)
    jsp_soup = _get_jsp_soup(mdcstat)

    valid_post_params = fetch.convert_vaild_post_params(jsp_soup, post_params)
    krx_data = fetch.get_krx_data(valid_post_params)

    korean_columns = column.get_korean_columns(jsp_soup, mdcstat)

    return get_dataframe(krx_data, korean_columns)


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


def _get_jsp_soup(mdcstat):
    """
    jsp_soup will be used for getting korean columns, valid_post_params.

    Parameters
    ----------
    mdcstat : str

    Returns
    -------
    jsp_soup : bs4.BeautifulSoup

    """
    jsp_filename = mdcstat[:-2]
    if _is_file(jsp_filename):
        jsp_soup = webio.soup(_load_jsp(jsp_filename))
    else:
        url = f"http://data.krx.co.kr/contents/MDC/STAT/standard/{jsp_filename}.jsp"
        jsp_soup = webio.get(url)
        _save_jsp(jsp_filename, jsp_soup)
    return jsp_soup


"""
자주 사용하는 기능의 jsp 파일은 저장해서 불러오는 걸로 사용하자.
server에 2번 요청하지 않도록.
"""

FILE_PATH = os.path.dirname(os.path.realpath(__file__))


def _is_file(jsp_filename):
    path = os.path.join(FILE_PATH, f'core/jsp/{jsp_filename}.jsp')
    return os.path.isfile(path)


def _save_jsp(jsp_filename, jsp_soup):
    path = os.path.join(FILE_PATH, f'core/jsp/{jsp_filename}.jsp')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(jsp_soup))


def _load_jsp(jsp_filename):
    path = os.path.join(FILE_PATH, f'core/jsp/{jsp_filename}.jsp')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
