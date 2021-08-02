import os
import requests

import pandas as pd

__url = "http://15.165.18.200:8080/"


def _requests_with_retry(url):
    for _ in range(5):
        try:
            retry = False
            response = requests.get(url, timeout=15).json()
        except requests.exceptions.ReadTimeout:
            retry = True
            response = {"msg": "Error : requests.exceptions.ReadTimeout"}
        if retry:
            continue
        else:
            break
    return response


def read(symbol, start, end, kind, resource, api_key):
    """

    Parameters
    ----------
    symbol : str
        조회하고자 하는 데이터의 종목코드.
        형태는 종목과 종류마다 다르다. 예) 삼성전자 : '005930', ARIRANG 200 : '152100'
    kind : str, default "stock"
        조회하고자 하는 데이터의 종류.
    resource : str
        url 주소를 완성하기 위한 것으로 데이터의 출처값을 있다.
    api_key : str
        api key
    start : str
        조회하고자 하는 데이터의 시작일.
        형태는 YYYY-MM-DD가 되어야 한다. 예) 2021-06-01
    end : str
        조회하고자 하는 데이터의 종료일.
        형태는 YYYY-MM-DD가 되어야 한다. 예) 2021-06-01

    Returns
    -------
    pd.DataFrame
    """

    url = os.path.join(
        __url,
        resource,
        kind,
        "read",
        f"?symbol={symbol}&start={start}&end={end}&apikey={api_key}",
    )
    response = _requests_with_retry(url)
    if response.get("msg", False):
        return response

    data = response["data"]
    df = pd.DataFrame(data)
    df.index = df["date"]
    df.index.name = ""
    transformed = df.drop(["name", "market", "division", "date", "symbol"], axis="columns")

    return transformed


def read_all(symbol, kind, resource, api_key):
    """
    api를 사용해서 해당 종목의 데이터를 받는

    Parameters
    ----------
    symbol : str
        조회하고자 하는 데이터의 종목코드.
        형태는 종목과 종류마다 다르다. 예) 삼성전자 : '005930', ARIRANG 200 : '152100'
    kind : str, default "stock"
        조회하고자 하는 데이터의 종류.
    resource : str
        url 주소를 완성하기 위한 것으로 데이터의 출처값을 있다.
    api_key : str
        api key

    Returns
    -------
    pd.DataFrame

    """
    url = os.path.join(
        __url, resource, kind, "read-all", f"?symbol={symbol}&apikey={api_key}"
    )
    response = _requests_with_retry(url)
    if response.get("msg", False):
        return response

    data = response["data"]
    df = pd.DataFrame(data)
    df.index = df["date"]
    df.index.name = ""
    transformed = df.drop(["name", "market", "division", "date", "symbol"], axis="columns")

    return transformed


def read_date(date, kind, resource, api_key):
    """
    api를 사용해서 해당 일자의 전 종목 데이터를 받는다.

    Parameters
    ----------
    date : str
        조회하고자 하는 데이터의 조회일.
        형태는 YYYY-MM-DD가 되어야 한다. 예) 2021-06-01
    kind : str, default "stock"
        조회하고자 하는 데이터의 종류.
    resource : str
        url 주소를 완성하기 위한 것으로 데이터의 출처값을 있다.
    api_key : str
        api key

    Returns
    -------
    pd.DateFrame

    """

    url = os.path.join(
        __url, resource, kind, "read-date", f"?date={date}&apikey={api_key}"
    )
    response = _requests_with_retry(url)
    if response.get("msg", False):
        return response
    data = response["data"]
    return pd.DataFrame(data)
