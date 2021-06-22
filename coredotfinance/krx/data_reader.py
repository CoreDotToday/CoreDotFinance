import os

from coredotfinance.krx.process import get_dataframe
from coredotfinance.krx.classify import get_krx_instance
from coredotfinance.krx import webio
from coredotfinance.krx import fetch
from coredotfinance.krx import column

FILE_PATH = os.path.dirname(os.path.realpath(__file__))


def data_reader(
    code, symbol=None, start=None, end=None, date=None, **kwargs
):
    """
    data_reader는 data.krx.co.kr로 부터 데이터를 가져온다.
    불러온 데이터는 Json 형태이며 key 값은 영문약자로 되어 있다.
    영문약자를 한글로 바꾸어 주기위해 data.krx.co.kr에서 .jsp 퍄일을 가져온다.
    .jsp 파일의 url을 얻기위해서는 'MDCSTAT' 으로 시작하는 쿼리 단어를 얻어야 하고
    그 단어는 post_params의 'bld' 값에 들어 있다.

    Parameters
    ----------
    code : str
        수행하고자 하는 krx의 기능번호
    start : str
    end : str
    symbol : str
        종목코드
    date : str
       조회일
    Returns
    -------

    """
    krx_instance = get_krx_instance(code, symbol=symbol, start=start, end=end, date=date, **kwargs)
    post_params = krx_instance.get_requested_data()
    if symbol:
        symbol_name = krx_instance.data_nm
        print(symbol_name)

    mdcstat = parse_mdcstat(post_params)
    jsp_soup = get_jsp_soup(mdcstat)

    valid_post_params = fetch.convert_vaild_post_params(jsp_soup, post_params)
    krx_data = fetch.get_krx_data(valid_post_params)

    korean_columns = column.get_korean_columns(jsp_soup, mdcstat)

    return get_dataframe(krx_data, korean_columns)


def parse_mdcstat(post_params):
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


def get_jsp_soup(mdcstat):
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
    if is_file(jsp_filename):
        jsp_soup = webio.soup(load_jsp(jsp_filename))
    else:
        url = f"http://data.krx.co.kr/contents/MDC/STAT/standard/{jsp_filename}.jsp"
        jsp_soup = webio.get(url)
        save_jsp(jsp_filename, jsp_soup)
    return jsp_soup


def is_file(jsp_filename):
    path = os.path.join(FILE_PATH, f'jsp/{jsp_filename}.jsp')
    return os.path.isfile(path)


def save_jsp(jsp_filename, jsp_soup):
    path = os.path.join(FILE_PATH, f'jsp/{jsp_filename}.jsp')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(jsp_soup))


def load_jsp(jsp_filename):
    path = os.path.join(FILE_PATH, f'jsp/{jsp_filename}.jsp')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
