# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from finance.statistics.basic.info import Info

class Bond(Info):
    def __init__(self, code, start, end, day, product, code_to_function):
        super(Bond, self).__init__(start, end, day)
        self.function = code_to_function[code]
        self.data_cd, self.data_nm, self.data_tp = self.autocomplete(product)

    def autocomplete(self, product):
        if product is None:
            return None, None, None
        auto_complete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_bondisu&value={product}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_bondisu_autocomplete'
        response = requests.get(auto_complete_url.format(product=product))
        soup = bs(response.content, 'html.parser').li

        if soup is None:
            raise ValueError(f'{product} is Wrong name as a product')

        print(soup.attrs['data-nm'])
        return soup.attrs['data-cd'], soup.attrs['data-nm'], soup.attrs['data-tp']




class ItemPrice(Bond):
    def __init__(self, code, start, end, day, product, **kwargs):
        code_to_function = {
            '14001': self.price_of_entire_item,
            '14002': self.price_trend_of_item
        }
        super().__init__(code, start, end, day, product, code_to_function)
        market_map = {
            '국채전문유통시장': 'KTS',
            '일반채권시장': 'BND',
            '소액채권시장': 'SMB'
        }
        self.market = market_map[kwargs.get('market', None)]
        self.market_1 = kwargs.get('market', None)

    def price_of_entire_item(self):
        """전종목 시세 [14001]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT09801',
            'mktId': self.market,
            'trdDd': self.day
            }
        return self.requests_data(data)

    def price_trend_of_item(self):
        """개별종목 시세 추이 [14002]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT09901',
            'mktId': self.market_1,
            'isuCd': self.data_cd,
            'tboxisuCdBox0_finder_bondisu0_2': self.data_nm,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)


class ItemInfo(Bond):
    pass


class TradePerform(Bond):
    pass


class Detail(Bond):
    pass