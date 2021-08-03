import os

from coredotfinance.krx.core import webio


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
    path = os.path.join(FILE_PATH, f"jsp/{jsp_filename}.jsp")
    return os.path.isfile(path)


def _save_jsp(jsp_filename, jsp_soup):
    path = os.path.join(FILE_PATH, f"jsp/{jsp_filename}.jsp")
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(jsp_soup))


def _load_jsp(jsp_filename):
    path = os.path.join(FILE_PATH, f"jsp/{jsp_filename}.jsp")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
