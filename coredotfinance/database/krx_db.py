import os
import requests

import pandas as pd
import numpy as np

__url = 'http://13.124.198.252:8080/'


def read(symbol, start, end, kind, resource, api_key, **kwargs):
    whole = kwargs.get('whole', False)
    url = os.path.join(__url, resource, kind, 'read', f'?symbol={symbol}&apikey={api_key}')
    response = eval(requests.get(url).content)
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
    url = os.path.join(__url, resource, kind, 'readall', f'?date={date}&apikey={api_key}')
    response = requests.get(url).json()
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
