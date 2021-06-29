import os
import requests

import pandas as pd
import numpy as np

__url = 'http://13.124.198.252:8080/'


def read(symbol, start, end, kind, resource, whole=False):
    url = os.path.join(__url, resource, kind, 'read', f'?symbol={symbol}')
    data = eval(requests.get(url).content)['data']

    df = pd.DataFrame(data)
    df.index = df['날짜']
    df.index.name = ''
    transformed = df.drop(['종목명', '시장구분', '소속부', '날짜'], axis='columns')

    if not whole:
        transformed = transformed[np.logical_and(transformed.index >= start, transformed.index <= end)]
        print(start, end)
        print(np.logical_and(transformed.index >= start, transformed.index <= end))

    return transformed


def read_all(date, kind, resouce):
    url = os.path.join(__url, resouce, kind, 'readall', f'?date={date}')
    data = eval(requests.get(url).content)

    data_list = []
    length = len(data['data']['종목코드'])
    for i in range(length):
        data_dict = {}
        for key in data['data']:
            data_dict[key] = data['data'][key][str(i)]
        data_list.append(data_dict)

    return pd.DataFrame(data_list)
