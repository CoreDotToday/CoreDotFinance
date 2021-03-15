# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from finance.statistics.basic.info import Info


class Commodity(Info):  # 일반상품: 석유, 금, 배출
    def __init__(self, code, start, end, day, product, product_type, code_to_function):
        super(Commodity, self).__init__(start, end, day)
        self.function = code_to_function[code]
"""
    def autocomplete(self, product, product_type):
        if product is None:
            return None, None, None
        if product_type == 'oil':
            auto_complete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_etf&value={product}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_etf_autocomplete'
        elif product_type == 'gold':
            auto_complete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_etn&value={product}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_etn_autocomplete'
        elif product_type == 'carbonemission':
            auto_complete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_elw&value={product}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_elw_autocomplete'

        response = requests.get(auto_complete_url.format(product=product))
        soup = bs(response.content, 'html.parser').li

        if soup is None:
            raise ValueError(f'{product} is Wrong name as a product')
"""


class Oil(Commodity):  # 석유 [16101~16105]
    def __init__(self, code, start, end, day, product, **kwargs):
        code_to_function = {
            '16101': self.info_of_entire_items(),
            '16102': self.price_trend_of_item(),
            '16103': self.trade_performance_per_investor(),
            '16104': self.price_domestic_gasstation(),
            #  '16105': self.price_international(),
        }

        super(Oil, self).__init__(code, start, end, day, product, code_to_function)
        self.inqtpcd = kwargs.get('inqtpcd', None)  # inqTpCd: 1(기간합계), 2(일별추이)
        self.trdvolval = kwargs.get('trdvolval', None)  # trdVolVal: 1(거래량), 2(거래대금)
        self.bidasknet = kwargs.get('bidasknet', None)  # bidAskNet: 1(매도), 2(매수), 3(순매수)
        self.secugrpld = kwargs.get('secugrpld', None)  # secugrpld: GA(휘발유), DI(경유), KE(등유)

    def info_of_entire_items(self):  # [16101] 전종목 기본정보
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT14301',
            'secugrpld': self.secugrpld  # ALL(전체), GA(휘발유), DI(경유), KE(등유)
        }
        return self.requests_data(data)

    def price_trend_of_item(self):  # [16102] 유종별 시세 추이
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT14401',
            'secugrpld': self.secugrpld,
            'strtDd': self.start,
            'endDd': self.end,
            #  'share': 1,  # 1~3(L / 천L / 백만L)
            #  'money': 1,  # 1~4(원 / 천원 / 백만원 / 십억원)
        }
        return self.requests_data(data)

    def trade_performance_per_investor(self):  # [16103] 참가자별 거래실적
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT14501',
            'inqTpCd': self.inqtpcd,  # 1(기간합계), 2(일별추이)
            'trdVolVal': self.trdvolval,  # 1(거래량), 2(거래대금)
            'bidAskNet': self.bidasknet,  # 1(매도), 2(매수), 3(순매수)
            'secugrpId': self.secugrpld,  # GA(휘발유), DI(경유), KE(등유)
            'strtDd': self.start,
            'endDd': self.end,
            #  'share': 1,  # 1~3(L / 천L / 백만L)
            #  'money': 1,  # 1~4(원 / 천원 / 백만원 / 십억원)
        }
        return self.requests_data(data)

    def price_domestic_gasstation(self):  # [16104] 국내유가(주유소) 동향
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT14601',
            'secugrpId': self.secugrpld,  # GA(휘발유), DI(경유), KE(등유)
            'strtDd': self.start,
            'endDd': self.end,
            # 'otherUnit': 1(Won/L)
        }
        return self.requests_data(data)

    def price_international(self):  # [16105] 국제유가 동향
        pass


class Gold(Commodity):  # 금 [16201~16207]
    def __init__(self, code, start, end, day, product, **kwargs):
        code_to_function = {
            '16201': self.price_of_entire_items(),
            '16202': self.price_trend_of_item(),
            '16203': self.info_of_entire_items(),
            '16204': self.info_of_item(),
            '16205': self.trade_performance_per_investor(),
            '16206': self.block_trade(),
            '16207': self.price_international(),
        }

        super(Gold, self).__init__(code, start, end, day, product, code_to_function)
        self.kwargs = kwargs
        self.inqtpcd = self.kwargs.get('inqtpcd', None)  # inqTpCd: 1(기간합계), 2(일별추이)
        self.trdvolval = self.kwargs.get('trdvolval', None)  # trdVolVal: 1(거래량), 2(거래대금)
        self.bidasknet = self.kwargs.get('bidasknet', None)  # bidAskNet: 1(매도), 2(매수), 3(순매수)
        self.secugrpld = self.kwargs.get('secugrpld', None)  # secugrpld: GA(휘발유), DI(경유), KE(등유)
        self.isucd = self.kwargs.get('isucd', None)  # isuCd: 개별종목명 [예: KRD040200002(금 99.99K), KRD040201000(미니금 100g)]

    def price_of_entire_items(self):  # [16201] 전종목 시세
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT14901',
            'trdDd': self.day,
            #  'share': 1,  # 1~3(g / 천g / 백만g)
            #  'money': 1,  # 1~4(원 / 천원 / 백만원 / 십억원)
        }
        return self.requests_data(data)

    def price_trend_of_item(self):  # [16202] 개별종목 시세 추이
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15001',
            'isuCd': self.isucd,  # KRD040200002(금 99.99K), KRD040201000(미니금 100g)
            'strtDd': self.start,
            'endDd': self.end,
            #  'share': 1,  # 1~3(g / 천g / 백만g)
            #  'money': 1,  # 1~4(원 / 천원 / 백만원 / 십억원)
        }
        return self.requests_data(data)

    def info_of_entire_items(self):  # [16203] 전종목 기본정보
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15101',
        }
        return self.requests_data(data)

    def info_of_item(self):  # [16204] 개별종목 종합정보
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15201',
            'isuCd': self.isucd,  # KRD040200002(금 99.99K), KRD040201000(미니금 100g)
        }
        """ 데이터 총 3개
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15202',
            'isuCd': self.isucd,  # KRD040200002(금 99.99K), KRD040201000(미니금 100g)
        }
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15203',
            'isuCd': self.isucd,  # KRD040200002(금 99.99K), KRD040201000(미니금 100g)
        }
        """
        return self.requests_data(data)

    def trade_performance_per_investor(self):  # [16205] 투자자별 거래실
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15301',
            'inqTpCd': self.inqtpcd,  # 1(기간합계), 2(일별추이)
            'trdVolVal': self.trdvolval,  # 1(거래량), 2(거래대금)
            'bidAskNet': self.bidasknet,  # 1(매도), 2(매수), 3(순매수)
            'strtDd': self.start,
            'endDd': self.end,
            #  'share': 1,  # 1~3(g / 천g / 백만g)
            #  'money': 1,  # 1~4(원 / 천원 / 백만원 / 십억원)
        }
        return self.requests_data(data)

    def block_trade(self):  # [16206] 협의대량거래실적 추이
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15401',
            'strtDd': self.start,
            'endDd': self.end,
            #  'share': 1  # 1~3(g / 천g / 백만g)
        }
        return self.requests_data(data)

    def price_international(self):  # [16207] 국제금시세 동향
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT13901',
            'strtDd': self.start,
            'endDd': self.end,
        }
        """ 표 2개
                data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT13902',
            'strtDd': self.start,
            'endDd': self.end,
        """
        return self.requests_data(data)


class CarbonEmission(Commodity):  # 배출권 [16301~16304]

    def __init__(self, code, start, end, day, product, **kwargs):
        code_to_function = {
            '16301': self.price_of_entire_items(),
            '16202': self.price_trend_of_item(),
            '16303': self.info_of_entire_items(),
            '16304': self.info_of_item(),
        }

        super(CarbonEmission, self).__init__(code, start, end, day, product, code_to_function)
        self.kwargs = kwargs
        self.isucd = self.kwargs.get('isucd', None)  # isuCd: 개별종목명 [예: KRD050022007(KAU20), KRD050032105(KAU21)]

    def price_of_entire_items(self):  # [16301] 전종목 시세
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15601',
            'trdDd': self.day,
            #  'share': 1,  # 1~3(톤 / 천톤 / 백만톤)
            #  'money': 1,  # 1~4(원 / 천원 / 백만원 / 십억원)
        }

    def price_trend_of_item(self):  # [16302] 개별종목 시세 추이
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15701',
            'isuCd': self.isucd,  # KRD050022007(KAU20)
            'strtDd': self.start,
            'endDd': self.end,
            #  'share': 1,  # 1~3(톤 / 천톤 / 백만톤)
            #  'money': 1,  # 1~4(원 / 천원 / 백만원 / 십억원)
        }

    def info_of_entire_items(self):  # [16303] 전종목 기본정보
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15801',
        }

    def info_of_item(self):  # [16304] 개별종목 종합정보
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15901',
            'isuCd': self.isucd,  # KRD050022007(KAU20), KRD050032105(KAU21)
        }
        """ 데이터 총 3개
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15902',
            'isuCd': self.isucd, # KRD050022007(KAU20), KRD050032105(KAU21)
        }
        data = {
            'bld': 'dbms / MDC / STAT / standard / MDCSTAT15903',
            'isuCd': self.isucd, # KRD050022007(KAU20), KRD050032105(KAU21)
        }
        """
