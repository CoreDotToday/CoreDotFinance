# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from finance.statistics.basic.info import Info

class Bond(Info):
    def __init__(self, code, start, end, day, product, code_to_function):
        super(Bond, self).__init__(start, end, day)
        self.function = code_to_function[code]
        self.data_cd, self.data_nm, self.data_tp = self.autocomplete(product, code)

    def autocomplete(self, product, code):
        if product is None:
            return None, None, None
        if code in ['14011']:
            auto_complete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_bndordisu' \
                                '&value={product}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder' \
                                '%2Ffinder_bndordisu_autocomplete'
        else:
            auto_complete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_bondisu' \
                                '&value={product}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder' \
                                '%2Ffinder_bondisu_autocomplete'
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
            'mktId': self.market_1,
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
    def __init__(self, code, start, end, day, product, **kwargs):

        code_to_function = {
            '14003': self.info_of_entire_item,
            '14004': ''
        }
        self.bond_type = kwargs.get('bond_type', None)
        super(ItemInfo, self).__init__(code, start, end, day, product, code_to_function)

    def info_of_entire_item(self):
        """전종목 기본정보 [14003]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT10001',
            'bndTpCd': self.bond_type
        }
        return self.requests_data(data)

    def entire_info_of_itme(self):
        """'개별종목 종합정보 [14004]"""
        '''not now'''


class TradePerform(Bond):
    def __init__(self, code, start, end, day, product, **kwargs):
        code_to_function = {
            '14005': self.trade_performance_per_category,
            '14006': self.trade_performance_per_investor,
            '14007': self.trade_performance_of_bond_index_item,
            '14008': self.trade_performance_of_Repo
        }
        super(TradePerform, self).__init__(code, start, end, day, product, code_to_function)
        self.market = kwargs.get('market', None)
        self.inquiry = kwargs.get('inquiry', None)

    def trade_performance_per_category(self):
        """종류별 거래실적 [14005]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT10201',
            'bndMktTpCd': self.market,
            'inqTpCd': self.inquiry,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def trade_performance_per_investor(self):
        """투자자별 거래실적 [14006]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT10301',
            'bndMktTpCd': self.market,
            'strtDd': self.start,
            'endDd': self.end,
        }
        return self.requests_data(data)

    def trade_performance_of_bond_index_item(self):
        """국채지표종목 거래실적 [14007]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT10401',
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)



    def trade_performance_of_Repo(self):
        """Repo 거래실적 [14008]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT10501',
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)


class Detail(Bond):
    def __init__(self, code, start, end, day, product, **kwargs):
        code_to_funciton = {
            '14009': self.price_assessment_trend_of_item,
            '14010': self.reported_price_trend_of_small_bond,
            '14011': self.search_of_public_bond,
            '14012': self.issue_info_of_public_bond,
            '14013': self.histoty_per_type_of_publication,
            '14014': self.history_of_publication_price_adjustment,
            '14015': self.prepayment,
            '14016': self.delisting_bond,
            '14017': self.rate_of_profit_of_bond_over_the_counter,
            '14018': self.rate_of_profit_of_index,
            '14019': self.strip_short_interest,
            '14020': self.substitution_price_of_bond,
            '14021': self.substitution_price_of_bond_per_issuer,
            '14022': self.substitution_price_of_bond_per_type,
            '14023': self.credit_per_issuer,
            '14024': self.publication_situation_per_credit,
            '14025': self.investment_index_of_convertible_bond,
            '14026': self.exercise_of_right_of_bond_about_stock,
            '14027': self.strike_price_of_bond_about_stock
        }
        super().__init__(code, start, end, day, product, code_to_funciton)
        self.market = kwargs.get('market', None)
        self.inquiry = kwargs.get('inquiry', None)
        self.bond_type = kwargs.get('bond_type', None)

    def price_assessment_trend_of_item(self):
        """개별종목 시가평가 추이 [14009]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT10601',
            'tboxisuCd_finder_bondisu0_0': f'{self.data_cd}/{self.data_nm}',
            'isuCd': self.data_cd,
            'codeNmisuCd_finder_bondisu0_0': self.data_nm,
            'param1isuCd_finder_bondisu0_0': 2,
            'basddTpCd': self.inquiry,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def reported_price_trend_of_small_bond(self):
        """소액채권 신고가격 추이 [14010]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT10701',
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def search_of_public_bond(self):
        """상장채권 상세검색 [14011]"""
        # 기능중 채권분류 및 상세검색은 추가하지 않았음
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT10801',
            'tboxisurCd_finder_bndordisu0_2': f'{self.data_tp}/{self.data_nm}',
            'isurCd': self.data_tp,
            'isurCd2': self.data_tp,
            'codeNmisurCd_finder_bndordisu0_2': self.data_nm,
            'bndTpCd': self.bond_type
        }
        return self.requests_data(data)

    def issue_info_of_public_bond(self):
        """상장채권 발행정보 [14012]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT10901',
            'tboxisuCd_finder_bondisu0_2': f'{self.data_cd}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_cd,
            'codeNmisuCd_finder_bondisu0_2': self.data_nm
        }
        return self.requests_data(data)

    def histoty_per_type_of_publication(self):
        """상장유형별 내역 [14013]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT11001',
            'inqTpCd': self.inquiry,
            'BndMktactTpCd': self.bond_type,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def history_of_publication_price_adjustment(self):
        """상장금액조정 내역 [14014]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT11101',
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def prepayment(self):
        """중도상환 [14015]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT11201',
            'bndMktactTpCd': self.inquiry,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def delisting_bond(self):
        """채권상장폐지 [14016]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT11301',
            'bndDelistRsnCd': self.inquiry,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def rate_of_profit_of_bond_over_the_counter(self):
        """장외 채권수익률 [14017]"""
        if self.inquiry == '개별추이':
            bld = 'dbms/MDC/STAT/standard/MDCSTAT11402'
        else:
            bld = 'dbms/MDC/STAT/standard/MDCSTAT11401'
        data = {
            'bld': bld,
            'inqTpCd': self.inquiry,
            'trdDd': self.day,
            'bndKindTpCd': self.bond_type,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def rate_of_profit_of_index(self):
        """지표 수익률 [14018]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT11501',
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def strip_short_interest(self):
        """스트립 단기금리 [14019]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT11601',
            'inqTpCd': self.inquiry,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def substitution_price_of_bond(self):
        """채권 대용가 [14020]"""????
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT11701',
            'searchType': self.inquiry,
            'tboxisuCd_finder_bondisu0_10': f'{self.data_cd}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_cd,
            'codeNmisuCd_finder_bondisu0_10': self.data_nm,
            'param1isuCd_finder_bondisu0_10': 2,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def substitution_price_of_bond_per_issuer(self):
        """발행기관별 채권 대용가 [14021]"""
        pass

    def substitution_price_of_bond_per_type(self):
        """유형별 채권 대용가 [14022]"""
        pass

    def credit_per_issuer(self):
        """발행기관별 신용등급 [14023]"""
        pass

    def publication_situation_per_credit(self):
        """신용등급별 상장현황 [14024]"""
        pass

    def investment_index_of_convertible_bond(self):
        """전환사채 투자지표 [14025]"""
        pass

    def exercise_of_right_of_bond_about_stock(self):
        """주식관련채권 권리행사 [14026]"""
        pass

    def strike_price_of_bond_about_stock(self):
        """주식관련채권 행사가액 [14027]"""
        pass

