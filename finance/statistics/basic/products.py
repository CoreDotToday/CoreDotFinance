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
        self.product = product
        self.data_cd, self.data_nm, self.data_tp = self.init_product_(product)

    def init_product_(self, product):
        if product is None:
            return None, None, None

        auto_complete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_etf&value={product}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_etf_autocomplete'
        response = requests.get(auto_complete_url.format(product=product))
        soup = bs(response.content, 'html.parser').li

        if soup is None:
            raise ValueError(f'{product} is Wrong name as a product')

        print(soup.attrs['data-nm'])
        return soup.attrs['data-cd'], soup.attrs['data-nm'], soup.attrs['data-tp']


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
            '13108': self.portfolio_deposit_file,
            '13109': self.detail_of_ETF,
            '13110': self.result_of_active_ETF,
            '13111': self.incorporated_asset_of_active_ETF,
            '13112': self.trend_of_tracking_error,
            '13113': self.trend_of_differential,
            '13114': self.trend_of_closing_differential,
            '13115': self.risk_of_multi_ETF_trader,
            '13116': self.managing_index_and_security_of_multi_ETF,
            '13117': self.assessment_of_LP_per_quarter
        }

        super(ETF, self).__init__(code, start, end, day, product, code_to_function)
        self.kwargs = kwargs
        self.inquiry = self.kwargs.get('inquiry', None)
        self.val_vol = self.kwargs.get('val_vol', None)
        self.trade = self.kwargs.get('trade', None)

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
        """
        전종목 등락률[13102]
        :arg
            start, end
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT04401',
            'strtDd': self.start,
            'endDd': self.end,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def price_trend_of_item(self):
        """
        개별종목 시세 추이[13103]
        :arg
            product, start, end
        """
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
        """
        투자자별 거래실적 [13106]
        :arg
            inquiry, val_vol, trade, start, end
        """
        inquiry_map = {
            '기간합계': 1,
            '일별추이': 2,
        }
        valvol_map = {
            '거래대금': 1,
            '거래량': 2,
        }
        trade_map = {
            '순매수': 1,
            '매수': 2,
            '매도': 3
        }
        if self.inquiry == '일별추이':
            val_vol = valvol_map[self.val_vol]
            trade = trade_map[self.trade]
        else:
            val_vol, trade = None, None

        inquiry = inquiry_map[self.inquiry]
        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0480{inquiry}',
            'inqTpCd': inquiry,
            'inqCondTpCd1': val_vol,
            'inqCondTpCd2': trade,
            'strtDd': self.start,
            'endDd': self.end,
            'money': 1
        }
        return self.requests_data(data)

    def trade_performance_per_investor_item(self):
        """
        투자자별 거래실적(개별종목) [13107]
        :arg
            inquiry, val_vol, trade, product, start, end
        """
        if self.product is None:
            raise ValueError(f'{self.product} is Wrong name as a product')
        inquiry_map = {
            '기간합계': 1,
            '일별추이': 2,
        }
        valvol_map = {
            '거래대금': 1,
            '거래량': 2,
        }
        trade_map = {
            '순매수': 1,
            '매수': 2,
            '매도': 3
        }
        if self.inquiry == '일별추이':
            val_vol = valvol_map[self.val_vol]
            trade = trade_map[self.trade]
        else:
            val_vol, trade = None, None

        inquiry = inquiry_map[self.inquiry]

        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0490{inquiry}',
            'inqTpCd': inquiry,
            'inqCondTpCd1': val_vol,
            'inqCondTpCd2': trade,
            'tboxisuCd_finder_secuprodisu1_4': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_cd,
            'codeNmisuCd_finder_secuprodisu1_4': self.data_nm,
            'strtDd': self.start,
            'endDd': self.end,
            'share': 1,
            'money': 1
            }
        return self.requests_data(data)


    def portfolio_deposit_file(self):
        """
        PDF (Porrfolio Deposit File) [13108]
        :arg
            product, day
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT05001',
            'tboxisuCd_finder_secuprodisu1_6': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_cd,
            'codeNmisuCd_finder_secuprodisu1_6': self.data_nm,
            'trdDd': self.day,
            'share': 1,
            'money': 1
            }
        return self.requests_data(data)

    def detail_of_ETF(self):
        """
        ETF 상세검색 [13109]
        Not now
        """
        pass

    def result_of_active_ETF(self):
        """
        액티브 ETF 실적 [13110]
        inquiry, product, start, end
        """
        inquiry_map = {
            '전종목': ['a', None],
            '개별종목': ['c', self.data_cd]
        }
        cls, isuCd = inquiry_map[self.inquiry]
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT05701',
            'cls': cls,
            'isuCd': isuCd,
            'strtDd': self.start,
            'endDd': self.end
            }
        return self.requests_data(data)

    def incorporated_asset_of_active_ETF(self):
        """
        액티브ETF 편입자산현황 [13111]
        :arg
            day, product, inquiry
        """
        inquiry_map = {
            '잔존만기': 1,
            '신용평가등급': 2
        }
        new_col_map_1 = {
            'NUM_ITM_VAL1': '1년 미만',
            'NUM_ITM_VAL2': '1년-5년',
            'NUM_ITM_VAL3': '5년-10년',
            'NUM_ITM_VAL4': '10년 이상',
            'NUM_ITM_VAL5': '채권 외 기타',
            'NUM_ITM_VAL6': '평균 잔존 만기'
        }
        new_col_map_2 = {
            'NUM_ITM_VAL1': 'RF(국고통안)',
            'NUM_ITM_VAL2': 'AAA',
            'NUM_ITM_VAL3': 'AA',
            'NUM_ITM_VAL4': 'A',
            'NUM_ITM_VAL5': 'BBB',
            'NUM_ITM_VAL6': 'BB',
            'NUM_ITM_VAL7': 'B 이하',
            'NUM_ITM_VAL8': '기타(CP, CD등)',
            'NUM_ITM_VAL9': '채권 외 기타',
        }
        inquiry = inquiry_map[self.inquiry]
        year = self.day[:4]
        month = self.day[4:6]
        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0580{inquiry}',
            'isuCd': self.data_cd,
            'startYear': year,
            'startMonth': month
        }
        new_col_map = new_col_map_1 if inquiry == 1 else new_col_map_2
        return self.requests_data(data, new_col_map)


    def trend_of_tracking_error(self):
        """
        추적오차율 추이 [13112]
        :arg
            product, start, end
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT05901',
            'isuCd': self.data_cd,
            'strtDd': self.start,
            'endDd': self.end
        }
        new_col_map = {
            'OBJ_STKPRC_IDX': '기초지수',
            'IDX_CHG_RTO': '기초지수변동률'
        }
        return self.requests_data(data, new_col_map)

    def trend_of_differential(self):
        """
        괴리율 추이 [13113]
        :arg
            product, start, end
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT06001',
            'isuCd': self.data_cd,
            'strtDd': self.start,
            'endDd': self.end
        }
        new_col_map = {
            'CLSPRC': '종가'
        }
        return self.requests_data(data, new_col_map)

    def trend_of_closing_differential(self):
        """
        장마감 괴리율 추이 [13114]
        :arg
            product, start, end
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT17101',
            'isuCd': self.data_cd,
            'strtDd': self.start,
            'endDd': self.end
        }

        return self.requests_data(data)


    def risk_of_multi_ETF_trader(self):
        """
        합성ETF 거래상대방 위험 [13115]
        :arg
            product, inquiry
        """
        inquiry_map = {
            '전종목': ['a', None],
            '개별종목': ['c', self.data_cd]
        }
        cls, isuCd = inquiry_map[self.inquiry]
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT06101',
            'cls': cls,
            'isuCd': isuCd,
            'strtDd': self.start,
            'endDd': self.end,
            'money': 1
        }
        return self.requests_data(data)


    def managing_index_and_security_of_multi_ETF(self):
        """
        합성ETF 기초지수 및 담보관리[13116]
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT06201'
        }
        return self.requests_data(data)

    def assessment_of_LP_per_quarter(self):
        """분기별 LP 평가[]13117"""
        '''Web page error '''
        pass

class ETN(Product):
    def __init__(self):

        code_to_function = {
            '13101': self.price_of_entire_items,
            '13102': self.fluc_of_entire_items,
            '13103': self.price_trend_of_item,
            '13104': self.info_of_entire_items,
            '13105': self.info_of_item,
            '13106': self.trade_performance_per_investor,
            '13107': self.trade_performance_per_investor_item
        }

    def price_of_entire_items(self):
        """
        전종목 시세 [13201]
        """
        pass

    def fluc_of_entire_items(self):
        """
        전종목 등락률 [13202]
        """
        pass

    def price_trend_of_item(self):
        """
        개별종목 시세추이 [13203]
        """
        pass

    def info_of_entire_items(self):
        """
        전종목 기본정보 [13204]
        """
        pass

    def info_of_item(self):
        """
        개별종목 종합정보 [13205]
        """
        pass

    def trade_performance_per_investor(self):
        """
        투자자별 거래실적 [13206]
        """
        pass

    def trade_performance_per_investor_item(self):
        """
        투자자별 거래실적(개별종목) [13207]
        """
        pass

    def detail_of_ETN(self):
        """
        ETN 상세검색 [13208]
        """
        pass

    def product_consisting_of_index(self):
        """
        기초지수 구성요소 [13209]
        """
        pass

    def credit_and_NCR(self):
        """
        발행사 신용등급 및 NCR [13210]
        """
        pass

    def risk_of_credit(self):
        """
        발행사 신용위험지표 [13211]
        """
        pass

    def condition_of_early_repayment_loss_limited_ETN(self):
        """
        손실제한ETN 조기상환 조건 [13212]
        """
        pass

    def consideration_of_range_accurual_of_loss_limited_ETN(self):
        """
        손실제한ETN 레인지어쿠루얼 참고사항 [13213]
        """
        pass

    def trend_of_differential(self):
        """
        괴리율 추이 [13214]
        """
        pass


    '13114': self.trend_of_closing_differential,
    '13115': self.risk_of_multi_ETF_trader,
    '13116': self.managing_index_and_security_of_multi_ETF,
    '13117': self.assessment_of_LP_per_quarter