import json
from datetime import datetime

import requests



class Index:
    def __init__(self, code, start, end, division):
        self.code = code
        if start is None:
            self.start = datetime.now().strftime('%Y%m%d')
        else:
            self.start = start
        self.end = end
        if division is None:
            self.division = '01'
        else:
            self.division = division.upper()
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'
        }
        self.url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'


    def requests_data(self, data):
        r = requests.post(self.url, data=data, headers=self.headers)
        data = json.loads(r.content)
        return data


class Stock(Index):
    def __init__(self, code, start, end, division):
        super(Stock, self).__init__(code, start, end, division)

        code_to_function = {
            11001: self.price_of_entire_index,
            11002: self.b
        }
        self.division_to_number = {
            'KRX': '01',
            'KOSPI': '02',
            'KOSDAQ': '03',
            'THEME': '04'
        }

        self.function = code_to_function[code]

    # 전체 지수 시세 110011
    def price_of_entire_index(self):
        data = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00101',
            'idxIndMidclssCd': self.division_to_number[self.division],
            'trdDd': self.start,
            'share': 1,
            'money': 1,
            'csvxls_isNo': 'false'
        }
        return self.requests_data(data)

    # 110012
    def b(self):
        pass

    def read(self):
        return self.function()



class Bond:
    pass