# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from finance.statistics.basic.info import Info

class Product(Info):
    def __init__(self, code, start, end, day, product, code_to_function):
        """
        증권상품
        :param code:
        :param start:
        :param end:
        :param day:
        :param product:
        :param code_to_function:
        """
        super(Product, self).__init__(start, end, day)
        self.function = code_to_function[code]
        self._find_product_data(product)

    def _find_product_data(self, product):
        if product is None:
            product = 'Arirang 200'
        auto_complete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_etf&value={product}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_etf_autocomplete'
        response = requests.get(auto_complete_url.format(product=product))
        soup = bs(response.content, 'html.parser').li

        if soup is None:
            raise AttributeError(f'{product} is Wrong name as a product')

        self.data_nm = soup.attrs['data-nm']
        self.data_cd = soup.attrs['data-cd']
        self.data_tp = soup.attrs['data-tp']


class ETF(Product):
    def __init__(self, code, start, end, day, product, **kwargs):
        """
        증권 상품
        :param code:
        :param start:
        :param end:
        :param day:
        :param product_name:
        :param search_type:
        """
        code_to_function = {
            '13101': self.price_of_entire_items,
            '13102': self.fluc_of_entire_items,
            '13103': self.price_trend_of_item,
            '13104': self.info_of_entire_items,
            '13105': self.info_of_item,
            '13106': self.trade_performance_per_investor,
            '13107': self.trade_performance_per_investor_item,
            '13108': self.portfolio_deposit_file
        }
        super(ETF, self).__init__(code, start, end, day, product, code_to_function)
        self.kwargs = kwargs


    def price_of_entire_items(self):
        """
        전종목 시세[13101]
        :arg
            day
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT04301',
            'trdDd': self.day,
            'share': 1,
            'money': 1
        }
        return self.requests_data(data)

    def fluc_of_entire_items(self):
        """전종목 등락률[13102]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT04401',
            'strtDd': self.start,
            'endDd': self.end,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def price_trend_of_item(self):
        """개별종목 시세 추이[13103]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT04501',
            'tboxisuCd_finder_secuprodisu1_31': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_cd,
            'codeNmisuCd_finder_secuprodisu1_31': self.data_nm,
            'strtDd': self.start,
            'endDd': self.end,
            'share': 1,
            'money': 1
        }
        return self.requests_data(data)

    def info_of_entire_items(self):
        """전종목 기본정보[13104]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT04601',
            'share': 1
            }
        return self.requests_data(data)

    def info_of_item(self):
        """개별종목 종합정보[13105]"""
        '''Not now'''
        pass

    def trade_performance_per_investor(self):
        """투자자별 거래실적 [13106]"""
        inquiry_map = {
            '기간합계': 1,
            '일별추이': 2,
            '거래량': 2,
            '거래대금': 1,
            '순매수': 1,
            '매수': 2,
            '매도': 3
        }

        inquiry_ = self.kwargs.get('inquiry', None)
        inquiry = inquiry_map[inquiry_]
        val_vol = self.kwargs.get('val_vol', None)  # 거래량/ 거래대금
        trade = self.kwargs.get('trade', None)  # 매수/ 매도/ 순매수

        if inquiry_ == '일별추이':
            val_vol = inquiry_map[val_vol]
            trade = inquiry_map[trade]

        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT04802',
            'inqTpCd': inquiry,
            'inqCondTpCd1': val_vol,
            'inqCondTpCd2': trade,
            'strtDd': self.start,
            'endDd': self.end,
            'money': 1
        }
        return self.requests_data(data)

    def trade_performance_per_investor_item(self):
        """투자자별 거래실적(개별종목) [13107]"""
        pass

    def portfolio_deposit_file(self):
        """PDF (Porrfolio Deposit File) [13108]"""
        pass
