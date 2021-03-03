# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from finance.statistics.basic.info import Info

class Product(Info):
    def __init__(self, code, start, end, day, product, product_type, code_to_function):
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
        self.data_cd, self.data_nm, self.data_tp = self.init_product_(product, product_type)

    def init_product_(self, product, product_type):
        if product is None:
            return None, None, None
        if product_type == 'etf':
            auto_complete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_etf&value={product}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_etf_autocomplete'
        elif product_type == 'etn':
            auto_complete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_etn&value={product}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_etn_autocomplete'
        elif product_type == 'elw':
            auto_complete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_secuprodisu_elw&value={product}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_secuprodisu_elw_autocomplete'

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

        super(ETF, self).__init__(code, start, end, day, product, 'etf', code_to_function)
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
    def __init__(self, code, start, end, day, product, **kwargs):

        code_to_function = {
            '13201': self.price_of_entire_items,
            '13202': self.fluc_of_entire_items,
            '13203': self.price_trend_of_item,
            '13204': self.info_of_entire_items,
            '13205': self.info_of_item,
            '13206': self.trade_performance_per_investor,
            '13207': self.trade_performance_per_investor_item,
            '13208': self.detail_of_ETN,
            '13209': self.product_consisting_of_index,
            '13210': self.credit_and_NCR,
            '13211': self.risk_of_credit,
            '13212': self.condition_of_early_repayment_loss_limited_ETN,
            '13213': self.consideration_of_range_accurual_of_loss_limited_ETN,
            '13214': self.trend_of_differential,
            '13215': self.trend_of_closing_differential
        }
        super(ETN, self).__init__(code, start, end, day, product, 'etn', code_to_function)
        self.kwargs = kwargs
        self.inquiry = self.kwargs.get('inquiry', None)
        self.val_vol = self.kwargs.get('val_vol', None)
        self.trade = self.kwargs.get('trade', None)
        self.issuing = self.kwargs.get('issuing', None)


    def price_of_entire_items(self):
        """
        전종목 시세 [13201]
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT06401',
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def fluc_of_entire_items(self):
        """
        전종목 등락률 [13202]
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT06501',
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def price_trend_of_item(self):
        """
        개별종목 시세추이 [13203]
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT06601',
            'tboxisuCd_finder_secuprodisu2_5': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'codeNmisuCd_finder_secuprodisu2_5': self.data_nm,
            'strtDd': self.start,
            'endDd': self.end,
        }
        new_col_map = {
            'CMPPREVDD_IDX': '기초지수대비',
            'FLUC_TP_CD1': '기초지수증감',
            'IDX_FLUC_RT': '기초지수등락률',
            'OBJ_STKPRC_IDX': '기초지수종가'
        }
        return self.requests_data(data, new_col_map)

    def info_of_entire_items(self):
        """
        전종목 기본정보 [13204]
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT06701'
        }
        return self.requests_data(data)

    def info_of_item(self):
        """
        개별종목 종합정보 [13205]
        not now
        """
        pass

    def trade_performance_per_investor(self):
        """
        투자자별 거래실적 [13206]
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
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0690{inquiry}',
            'inqTpCd': inquiry,
            'inqCondTpCd1': val_vol,
            'inqCondTpCd2': trade,
            'strtDd': self.start,
            'endDd': self.end
        }

        return self.requests_data(data)

    def trade_performance_per_investor_item(self):
        """
        투자자별 거래실적(개별종목) [13207]
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
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0700{inquiry}',
            'inqTpCd': inquiry,
            'inqCondTpCd1': val_vol,
            'inqCondTpCd2': trade,
            'tboxisuCd_finder_secuprodisu2_10': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'codeNmisuCd_finder_secuprodisu2_10': self.data_nm,
            'strtDd': self.start,
            'endDd': self.end,
            'share': 1,
            'money': 1
        }
        return self.requests_data(data)

    def detail_of_ETN(self):
        """
        ETN 상세검색 [13208]
        not now
        """
        pass


    def product_consisting_of_index(self):
        """
        기초지수 구성요소 [13209]
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT07601',
            'tboxisuCd_finder_secuprodisu2_2': self.data_nm,
            'isuCd': self.data_cd,
            'isuCd2': self.data_tp,
            'codeNmisuCd_finder_secuprodisu2_2': self.data_nm,
            'trdDd': self.day
        }
        return self.requests_data(data)

    def credit_and_NCR(self):
        """
        발행사 신용등급 및 NCR [13210]
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT07701',
            'tboxisuCd_finder_secuprodisu2_3': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'codeNmisuCd_finder_secuprodisu2_3': self.data_nm
        }
        return self.requests_data(data)

    def risk_of_credit(self):
        """
        발행사 신용위험지표 [13211]
        """
        issuing_map = {
            "KB증권": "00345",
            "NH투자증권": "00594",
            "노무라": "12928",
            "대신증권": "00354",
            "미래에셋대우": "00680",
            "삼성증권": "01636",
            "신영증권": "00172",
            "신한투자": "00867",
            "한국증권": "03049",
        }
        issuing = issuing_map[self.issuing]
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT07801',
            'isurCd': issuing,
            'strtDd': self.start,
            'endDd': self.end
        }
        new_col_map = {
            'INDIC_VAL_AMT': 'ENT 매출',
            'INVST_HD_MKTCAP': 'ELW 매출',
            'AGG_VAL': '매출합계',
        }
        return self.requests_data(data, new_col_map)

    def condition_of_early_repayment_loss_limited_ETN(self):
        """
        손실제한ETN 조기상환 조건 [13212]
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT07901',
            'isuCd': self.data_cd,
            'trdDd': self.day
        }
        new_col_map = {
            'IDX_IND_NM': '기초지수',
            'CLSPRC_IDX': '현재기초지수수준'

        }
        return self.requests_data(data, new_col_map)

    def consideration_of_range_accurual_of_loss_limited_ETN(self):
        """
        손실제한ETN 레인지어쿠루얼 참고사항 [13213]
        No data!!
        """
        pass

    def trend_of_differential(self):
        """
        괴리율 추이 [13214]
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT08101',
            'isuCd': self.data_cd,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def trend_of_closing_differential(self):
        """
        장마감 괴리율 추이 [13215]
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT17201',
            'isuCd': self.data_cd,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def assessment_of_LP_per_quarter(self):
        """분기별 LP 평가 [13216]"""
        '''Web page error '''
        pass

class ELW(Product):
    def __init__(self, code, start, end, day, product, **kwargs):
        code_to_function = {
            '13301': self.price_of_entire_items,
            '13302': self.trend_of_item,
            '13303': self.info_of_entire_items,
            '13304': self.entire_info_of_item,
            '13305': self.trade_performance_per_investor,
            '13306': self.trade_performance_per_basic_asset,
            '13307': self.item_of_residual_expiration_status,
            '13308': self.item_of_beneficial_expiration_status,
            '13309': self.approach_level_of_early_close,
            '13310': self.log_of_early_close,
            '13311': self.status_of_floating_per_basic_asset,
            '13312': self.status_of_floating_per_issuing,
            '13313': self.assessment_of_LP_per_quarter
        }
        super(ELW, self).__init__(code, start, end, day, product, 'elw', code_to_function)
        self.kwargs = kwargs
        self.inquiry = self.kwargs.get('inquiry', None)
        self.val_vol = self.kwargs.get('val_vol', None)
        self.trade = self.kwargs.get('trade', None)
        self.basic_asset = self.kwargs.get('basic_asset', None)

    def price_of_entire_items(self):
        """전종목 시세[13301]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT08301',
            'trdDd': self.day
        }
        new_col_map = {
            'LIST_SHRS': '상장증권수',
            'FLUC_TP_CD1': '증감',
            'CMPPREVDD_PRC1': '대비'
        }
        return self.requests_data(data, new_col_map)

    def trend_of_item(self):
        """개별종목 시세 추이[13302]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT08401',
            'tboxisuCd_finder_secuprodisu3_34': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_tp,
            'codeNmisuCd_finder_secuprodisu3_34': self.data_nm,
            'strtDd': self.start,
            'endDd': self.end
        }
        new_col_map = {
            'TDD_CLSPRC': '증감',
            'LIST_SHRS': '상장증권수',
            'CMPPREVDD_PRC1': '대비'
        }
        return self.requests_data(data, new_col_map)

    def info_of_entire_items(self):
        """전종목 기본정보[13303]
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT08501'
        }
        return self.requests_data(data)

    def entire_info_of_item(self):
        """개별종목 종합정보[13304]
        Not now"""
        pass

    def trade_performance_per_investor(self):
        """투자자별 거래실적[13305]"""
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
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0870{inquiry}',
            'inqTpCd': inquiry,
            'inqCondTpCd1': val_vol,
            'inqCondTpCd2': trade,
            'strtDd': self.start,
            'endDd': self.end
                }
        return self.requests_data(data)

    def trade_performance_per_basic_asset(self):
        """기초자산별 거래실적[13306]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT08801',
            'strtDd': self.start,
            'endDd': self.end
        }
        new_col_map = {
            'ISU_CNT1': 'CALL 종목수',
            'TRDVOL1': 'CALL 거래량',
            'TRDVAL1': 'CALL 거래대금',
            'ISU_CNT2': 'PUT 종목수',
            'TRDVOL2': 'PUT 거래량',
            'TRDVAL2': 'PUT 거래대금'
        }
        return self.requests_data(data, new_col_map)

    def item_of_residual_expiration_status(self):
        """개별종목 잔존만기현황[13307]"""
        inquiry_map = {
            '전체': 'T',
            '일반': 1,
            '조기종료': 2
        }
        if self.inquiry == None:
            inquiry = inquiry_map['전체']
        else:
            inquiry = inquiry_map[self.inquiry]
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT08901',
            'elwEoTpCd': inquiry,
            'trdDd': self.day
        }
        return self.requests_data(data)

    def item_of_beneficial_expiration_status(self):
        """개별종목 만기손익현황[13308]"""
        inquiry_map = {
            '전체': 'T',
            '일반': 1,
            '조기종료': 2
        }
        if self.inquiry == None:
            inquiry = inquiry_map['전체']
        else:
            inquiry = inquiry_map[self.inquiry]

        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT09001',
            'elwEoTpCd': inquiry,
            'strtDd': self.start,
            'endDd': self.end
        }
        new_col_map = {
            'ULY_NM2': '기초자산면'
        }
        return self.requests_data(data, new_col_map)


    def approach_level_of_early_close(self):
        """조기종료 접근[13309]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT09201',
            'trdDd': self.day
        }
        return self.requests_data(data)

    def log_of_early_close(self):
        """조기종료 발생내역[13310]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT09301',
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def status_of_floating_per_basic_asset(self):
        """기초자산별 상장현황[13311]"""
        inquiry_map = {
            '전체': 'T',
            '일반': 1,
            '조기종료': 2
        }
        if self.inquiry == None:
            inquiry = inquiry_map['전체']
        else:
            inquiry = inquiry_map[self.inquiry]

        basic_asset_map = {
            '유가증권시장': 1,
            '코스닥시장': 2,
            '해외지수': 9,
            '전체': 'T'
        }
        if self.basic_asset is None:
            basic_asset = basic_asset_map['전체']
        else:
            basic_asset = basic_asset_map[self.basic_asset]
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT09401',
            'elwRghtTpKindCd': inquiry,
            'elwUlyTpCd': basic_asset,
            'trdDd': self.day
        }
        new_col_map = {
            'CALL_CNT': '상장종목수/CALL',
            'PUT_CNT': '상장종목수/PUT',
            'ETC_CNT': '상장종목수/기타',
            'TOT_CNT': '상장종목수/합계',
            'CALL_TRDFORM_CNT': '거래형성종목수/CALL',
            'PUT_TRDFORM_CNT': '거래형성종목수/PUT'
        }
        return self.requests_data(data, new_col_map)

    def status_of_floating_per_issuing(self):
        """발행사별 상장현황[13312]"""
        inquiry_map = {
            '전체': 'T',
            '일반': 1,
            '조기종료': 2
        }
        if self.inquiry == None:
            inquiry = inquiry_map['전체']
        else:
            inquiry = inquiry_map[self.inquiry]
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT09501',
            'elwEoTpCd': inquiry,
            'trdDd': self.day
        }
        new_col_map = {
            'LIST_ISU_CNT1': '주식/CALL',
            'LIST_ISU_CNT2': '주식/PUT',
            'LIST_ISU_CNT3': '주식/합계',
            'LIST_ISU_CNT4': '주식바스켓/CALL',
            'LIST_ISU_CNT5': '주식바스켓/PUT',
            'LIST_ISU_CNT6': '주식바스켓/소계',
            'LIST_ISU_CNT7': '주가지수/CALL',
            'LIST_ISU_CNT8': '주가지수/PUT',
            'LIST_ISU_CNT9': '주가지수/소계',
            'LIST_ISU_CNT10': '합계/CALL',
            'LIST_ISU_CNT11': '합계/PUT',
            'LIST_ISU_CNT12': '합계/소계'
        }
        return self.requests_data(data, new_col_map)

    def assessment_of_LP_per_quarter(self):
        """분기별 LP 평가 [13313]"""
        '''Web page error '''
        pass
