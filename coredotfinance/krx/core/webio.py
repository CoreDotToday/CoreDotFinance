import requests
from bs4 import BeautifulSoup as bs


def get(url, params=None):
    """
    requests data to the server as get-type and returns bs4.BeautifulSoup

    Parameters
    ----------
    url : str
    params : dict

    Returns
    -------
    bs4.BeautifulSoup
    """
    res = requests.get(url, params=params)
    status_ok(res)
    return bs(res.content, "html.parser")


def post(url, data, headers=None, soup=False):
    """
    requests data to the server as post-type and returns bs4.BeautifulSoup.

    Parameters
    ----------
    url : str
    headers : dict
    data : dict

    Returns
    -------
    bs4.BeautifulSoup
    """
    res = requests.post(url, headers=headers, data=data)
    status_ok(res)
    if soup:
        return bs(res.content, "html.parser")
    else:
        return res


def soup(txt):
    return bs(txt, "html.parser")


def status_ok(res):
    if res.status_code != 200:
        raise ConnectionError(
            f"response is not 200 from the server.\nstatus_code : {res.status_code}"
        )
    else:
        pass
