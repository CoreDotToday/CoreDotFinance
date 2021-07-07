import os
import requests

import pandas as pd
import numpy as np

__url = 'http://52.79.172.205:8080/'

def _requests_with_retry(url):
    for _ in range(5):
        try:
            retry = False
            response = requests.get(url, timeout = 15).json()
        except requests.exceptions.ReadTimeout:
            retry = True
            response = {'msg' : 'Error : requests.exceptions.ReadTimeout'}
        if retry:
            continue
        else:
            break
    return response


def read(symbol, start, end, kind, resource, api_key, **kwargs):
    """
    api를 사용해서 해당 종목의 데이터를 받는

    Parameters
    ----------
    symbol : str
        조회하고자 하는 데이터의 종목코드.
        형태는 종목과 종류마다 다르다. 예) 삼성전자 : '005930', ARIRANG 200 : '152100'
    start : str
        조회하고자 하는 데이터의 시작일.
        형태는 YYYY-MM-DD가 되어야 한다. 예) 2021-06-01
    end : str
        조회하고자 하는 데이터의 종료일.
        형태는 YYYY-MM-DD가 되어야 한다. 예) 2021-06-01
    kind : str, default "stock"
        조회하고자 하는 데이터의 종류.
    api : bool, default False
        api_key가 설정되어 있지 않으면서 api가 True면 error가 발생한다.
        api 이용은 주식 가격만 가능하다.
    resource : str
        url 주소를 완성하기 위한 것으로 데이터의 출처값을 있다.
    api_key : str
        api key

    Returns
    -------
    pd.DataFrame

    """
    whole = kwargs.get('whole', False)
    url = os.path.join(__url, resource, kind, 'read', f'?symbol={symbol}&apikey={api_key}')
    response = _requests_with_retry(url)
    if response.get('msg', False):
        return response

    data = response['data']
    df = pd.DataFrame(data)
    df.index = df['날짜']
    df.index.name = ''
    transformed = df.drop(['종목명', '시장구분', '소속부', '날짜'], axis='columns')

    if not whole:
        transformed = transformed[np.logical_and(transformed.index >= start, transformed.index <= end)]

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

    url = os.path.join(__url, resource, kind, 'readall', f'?date={date}&apikey={api_key}')
    response = _requests_with_retry(url)
    if response.get('msg', False):
        return response

    data = response['data']
    data_list = []
    length = len(data['종목코드'])
    for i in range(length):
        data_dict = {}
        for key in data:
            data_dict[key] = data[key][str(i)]
        data_list.append(data_dict)

    return pd.DataFrame(data_list)
