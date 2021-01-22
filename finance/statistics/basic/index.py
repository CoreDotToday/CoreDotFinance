import json
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup as bs


class Index:
    def __init__(self, code, start, end, day, division, bond, ind_name, stc_name):
        today = datetime.now()
        a_month_ago = today - timedelta(days=30)
        self.code = code
        self.start = a_month_ago.strftime('%Y%m%d') if start is None else start
        self.end = today.strftime('%Y%m%d') if end is None else end
        self.day = today.strftime('%Y%m%d') if day is None else day
        self.division = 'KRX' if division is None else division.upper()
        self.bond = 'KRX채권' if bond is None else bond.upper()
        self.ind_name, self.indIdx, self.indIdx2 = self.find_index_data(ind_name)
        self.stc_name = stc_name


        self.division_category = {
            'KRX': '01',
            'KOSPI': '02',
            'KOSDAQ': '03',
            'THEME': '04'
        }

        self.bond_category = {
            'KRX채권': 1,
            'KTB지수': 2,
            '국고채프라임지수': 3
        }

        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'
        }
        self.url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'


    def requests_data(self, data):
        r = requests.post(self.url, data=data, headers=self.headers)
        data = json.loads(r.content)
        return data

    def find_index_data(self, ind_name):
        if ind_name is None:
            ind_name = 'krx'
        index_autocomplete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_equidx&value={value}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_equidx_autocomplete'
        response = requests.get(index_autocomplete_url.format(value=ind_name))
        soup = bs(response.content, 'html.parser').li

        if soup is None:
            raise AttributeError(f'{ind_name} is Wrong name as an index name')

        ind_name = soup.attrs['data-nm']
        indIdx = soup.attrs['data-cd']
        indIdx2 = soup.attrs['data-tp']

        return ind_name, indIdx, indIdx2

    def read(self):
        return self.function()


class Stock(Index):
    def __init__(self, code, start, end, day, division, bond, ind_name, stc_name):
        super(Stock, self).__init__(code, start, end, day, division, bond, ind_name, stc_name)

        code_to_function = {
            '11001': self.price_of_entire_index,
            '11002': self.fluc_of_entire_index,
            '11003': self.trend_of_index_price,
            '11004': self.info_of_entire_index,
            '11005': 'Not now',
            '11006': self.stocks_of_index,
            '11007_a': self.per_pbr_dividend_of_entire_index,
            '11007_b': self.per_pbr_dividend_of_index
        }


        self.function = code_to_function[code]


    # 전체 지수 시세 11001
    def price_of_entire_index(self):
        print(f'day : {self.day}')
        print(f'division : {self.division}')
        data = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00101',
            'idxIndMidclssCd': self.division_category[self.division],
            'trdDd': self.day,
            'share': 1,
            'money': 1,
            'csvxls_isNo': 'false'
        }
        return self.requests_data(data)

    # 전체 지수 변동률 11002
    def fluc_of_entire_index(self):
        print(f'str - end : {self.start} - {self.end}')
        print(f'division : {self.division}')
        data = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00201',
            'idxIndMidclssCd': self.division_category[self.division],
            'strtDd': self.start,
            'endDd': self.end,
            'share': '2',
            'money': '3',
            'csvxls_isNo': 'false'
        }
        return self.requests_data(data)

    # 전체 지수 변동률 11003
    def trend_of_index_price(self):
        if self.ind_name is None:
            raise ValueError('missing 1 required positional argument: \'ind_name\'')
        print(f'str - end : {self.start} - {self.end}')
        print(f'index_name : {self.ind_name}')
        data = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00301',
            'tboxindIdx_finder_equidx0_0': self.ind_name,
            'indIdx': self.indIdx,
            'indIdx2': self.indIdx2,
            'codeNmindIdx_finder_equidx0_0': self.ind_name,
            'strtDd': self.start,
            'endDd': self.end,
            'share': 2,
            'money': 3,
            'csvxls_isNo': 'false'
        }
        return self.requests_data(data)

    # 전체 지수 기본 정보 11004
    def info_of_entire_index(self):
        data = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00401',
            'idxIndMidclssCd': self.division_category[self.division],
            'csvxls_isNo': 'false'
        }
        return self.requests_data(data)

    # 개별 지수 종합 정보 11005
    def info_of_index(self):
        pass

    # 지구 구성 종목 11006
    def stocks_of_index(self):
        data = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00601',
            'tboxindIdx_finder_equidx0_2': self.ind_name,
            'indIdx': self.indIdx,
            'indIdx2': self.indIdx2,
            'codeNmindIdx_finder_equidx0_2': self.ind_name,
            'trdDd': self.day,
            'money': 3,
            'csvxls_isNo': 'false'
        }
        return self.requests_data(data)

    # PER/PBR/배당수익률 11007_a
    def per_pbr_dividend_of_entire_index(self):
        print(f'day : {self.day}')
        print(f'division : {self.division}')

        data = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00701',
            'searchType': 'A',
            'idxIndMidclssCd': self.division_category[self.division],
            'trdDd': self.day,
            'csvxls_isNo': 'false'
        }
        return self.requests_data(data)

    # PER/PBR/배당수익률 11007_b
    def per_pbr_dividend_of_index(self):
        print(f'str - end : {self.start} - {self.end}')
        print(f'index_name : {self.ind_name}')
        data = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00702',
            'searchType': 'P',
            'indTpCd': self.indIdx,
            'indTpCd2': self.indIdx2,
            'codeNmindTpCd_finder_equidx0_3': self.ind_name,
            'strtDd': self.start,
            'endDd': self.end,
            'csvxls_isNo': 'false'
        }
        return self.requests_data(data)


class Bond(Index):
    def __init__(self, code, start, end, day, division, bond, ind_name, stc_name):
        super(Bond, self).__init__(code, start, end, day, division, bond, ind_name, stc_name)

        code_to_function = {
            '11008': self.price_of_entire_index,
            '11009': self.trend_of_index
        }

        self.function = code_to_function[code]

    # 전체 지수 시세 11008
    def price_of_entire_index(self):
        data = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00801',
            'trdDd': self.day,
            'csvxls_isNo': 'false'
        }
        return self.requests_data(data)

    # 개별 지수 시세 추이 11009
    def trend_of_index(self):
        data = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00901',
            'indTp': self.bond_category[self.bond],
            'strtDd': self.start,
            'endDd': self.end,
            'csvxls_isNo': 'false'
        }
        return self.requests_data(data)


class Derivation(Index):
    def __init__(self, code, start, end, day, division, ind_name, stc_name):
        super(Derivation, self).__init__(code, start, end, day, division, ind_name, stc_name)
