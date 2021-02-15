# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from finance.statistics.basic.info import Info

class Index(Info):
    pass


class StockIndex(Index):
    def __init__(self, code, start, end, day, division, ind_name):
        """ 주가지수
        :param code: 항목 고유 번호
        :param start: 시작일
        :param end: 종료일
        :param day: 조회일자
        :param division:
        :param ind_name:
        """
        super(StockIndex, self).__init__(code, start, end, day)

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

        self.division_category = {
            'KRX': '01',
            'KOSPI': '02',
            'KOSDAQ': '03',
            'THEME': '04'
        }

        self.ind_name, self.indIdx, self.indIdx2 = self._find_index_data(ind_name)
        self.division = 'KRX' if division is None else division.upper()
        self.function = code_to_function[code]

    def _find_index_data(self, ind_name):
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


    def price_of_entire_index(self):
        """전체 지수 시세 [11001]"""
        print(f'day : {self.day}')
        print(f'division : {self.division}')
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00101',
            'idxIndMidclssCd': self.division_category[self.division],
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def fluc_of_entire_index(self):
        """전체 지수 변동률 [11002]"""
        print(f'str - end : {self.start} - {self.end}')
        print(f'division : {self.division}')
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00201',
            'idxIndMidclssCd': self.division_category[self.division],
            'strtDd': self.start,
            'endDd': self.end,
            'share': '2',
            'money': '3'
        }
        return self.requests_data(data)

    def trend_of_index_price(self):
        """개별 지수 시세추이 [11003]"""
        if self.ind_name is None:
            raise ValueError('missing 1 required positional argument: \'ind_name\'')
        print(f'str - end : {self.start} - {self.end}')
        print(f'index_name : {self.ind_name}')
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00301',
            'tboxindIdx_finder_equidx0_0': self.ind_name,
            'indIdx': self.indIdx,
            'indIdx2': self.indIdx2,
            'codeNmindIdx_finder_equidx0_0': self.ind_name,
            'strtDd': self.start,
            'endDd': self.end,
            'share': 2,
            'money': 3
        }
        return self.requests_data(data)

    def info_of_entire_index(self):
        """전체 지수 기본 정보 [11004]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00401',
            'idxIndMidclssCd': self.division_category[self.division]
        }
        return self.requests_data(data)


    def info_of_index(self):
        """개별 지수 종합 정보 [11005]"""
        pass

    def stocks_of_index(self):
        """지구 구성 종목 [11006]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00601',
            'tboxindIdx_finder_equidx0_2': self.ind_name,
            'indIdx': self.indIdx,
            'indIdx2': self.indIdx2,
            'codeNmindIdx_finder_equidx0_2': self.ind_name,
            'trdDd': self.day,
            'money': 3
        }
        return self.requests_data(data)

    def per_pbr_dividend_of_entire_index(self):
        """전체지수 : PER/PBR/배당수익률 [11007_a]"""
        print(f'day : {self.day}')
        print(f'division : {self.division}')

        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00701',
            'searchType': 'A',
            'idxIndMidclssCd': self.division_category[self.division],
            'trdDd': self.day
        }
        return self.requests_data(data)

    def per_pbr_dividend_of_index(self):
        """개별지수 PER/PBR/배당수익률 [11007_b]"""
        print(f'str - end : {self.start} - {self.end}')
        print(f'index_name : {self.ind_name}')
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00702',
            'searchType': 'P',
            'indTpCd': self.indIdx,
            'indTpCd2': self.indIdx2,
            'codeNmindTpCd_finder_equidx0_3': self.ind_name,
            'strtDd': self.start,
            'endDd': self.end,
        }
        return self.requests_data(data)


class BondIndex(Index):
    def __init__(self, code, start, end, day, division):
        """
        :param code:
        :param start:
        :param end:
        :param day:
        :param division:
        """
        super(BondIndex, self).__init__(code, start, end, day)

        code_to_function = {
            '11008': self.price_of_entire_index,
            '11009': self.trend_of_index
        }

        self.division_category = {
            'KRX채권': 1,
            'KTB지수': 2,
            '국고채프라임지수': 3
        }
        self.division = 'KRX채권' if division is None else division.upper()
        self.function = code_to_function[code]

    def price_of_entire_index(self):
        """전체 지수 시세 [11008]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00801',
            'trdDd': self.day,
        }
        return self.requests_data(data)

    def trend_of_index(self):
        """개별 지수 시세 추이 [11009]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT00901',
            'indTp': self.division_category[self.division],
            'strtDd': self.start,
            'endDd': self.end,
        }
        return self.requests_data(data)


class DerivationIndex(Index):
    def __init__(self, code, start, end, day, division, ind_name):
        super(DerivationIndex, self).__init__(code, start, end, day)

        code_to_function = {
            '11010': self.price_of_entire_index,
            '11011': self.fluc_of_entire_index,
            '11012': self.trend_of_index,
            '11013': self.info_of_entire_index,
            '11014': 'Not now'
        }

        self.division_clssCd = {
            '선물지수': '0201',
            '옵션지수': '0202',
            '전략지수': '0300',
            '상품지수': '0600'
        }
        self.ind_name, self.indIdx, self.indIdx2 = self._find_index_data(ind_name)
        self.division = '선물지수' if division is None else division.upper()
        self.function = code_to_function[code]

    def _find_index_data(self, ind_name):
        if ind_name is None:
            ind_name = '코스피 200 선물지수'
        index_autocomplete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_drvetcidx&value={value}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_drvetcidx_autocomplete'
        response = requests.get(index_autocomplete_url.format(value=ind_name))
        soup = bs(response.content, 'html.parser').li

        if soup is None:
            raise AttributeError(f'{ind_name} is Wrong name as an index name')

        ind_name = soup.attrs['data-nm']
        indIdx = soup.attrs['data-cd']
        indIdx2 = soup.attrs['data-tp']

        return ind_name, indIdx, indIdx2

    def price_of_entire_index(self):
        """ 전체 지수 시세 [11010] """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01001',
            'clssCd': self.division_clssCd[self.division],
            'trdDd': self.day,
        }
        return self.requests_data(data)

    def fluc_of_entire_index(self):
        """전체 지수 등락률 [11011]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01101',
            'clssCd': self.division_clssCd[self.division],
            'strtDd': self.start,
            'endDd': self.end,
        }
        return self.requests_data(data)

    def trend_of_index(self):
        """ 개별 지수 시세 추이 [11012] """
        print(self.ind_name)
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01201',
            'indTpCd': self.indIdx,
            'idxIndCd': self.indIdx2,
            'tboxidxCd_finder_drvetcidx0_0': self.ind_name,
            'idxCd': self.indIdx,
            'idxCd2': self.indIdx2,
            'codeNmidxCd_finder_drvetcidx0_0': self.ind_name,
            'strtDd': self.start,
            'endDd': self.end,
        }
        return self.requests_data(data)

    def info_of_entire_index(self):
        """ 전체 지수 기본 정보 [11013] """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01301',
            'idxTp': self.division_clssCd[self.division],
        }
        return self.requests_data(data)




