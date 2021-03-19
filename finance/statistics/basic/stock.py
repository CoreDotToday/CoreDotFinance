# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from finance.statistics.basic.info import Info

class Stock(Info):
    def __init__(self, code, code_to_function, division, item, start, end, day, **kwargs):
        """
        주가
        :param code:
        :param start:
        :param end:
        :param day:
        :param division:
        :param item:
        """
        super(Stock, self).__init__(start, end, day)
        item_code = kwargs.get('item_code', None)
        if item_code:
            item = self.convert_code_to_name(item_code)
        self.data_nm, self.data_cd, self.data_tp = self.autocomplete(item)
        self.division = '전체' if division is None else division.upper()
        self.function = code_to_function[code]
        self.detail = kwargs.get('detail', None)
        self.trade_index = kwargs.get('trade_index', None)
        self.trade_check = kwargs.get('trade_check', None)



    def autocomplete(self, item):
        if item is None:
            # 나중에 고쳐야함. item 이 필요한 함수들은 item이 없을 때 item이 없음을 알릴 필요가 있음.
            item = '삼성전자'
        stock_autocomplete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_stkisu&value={value}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_stkisu_autocomplete'
        response = requests.get(stock_autocomplete_url.format(value=item))
        soup = bs(response.content, 'html.parser').li

        if soup is None:
            raise AttributeError(f'{item} is Wrong name as a stock name')

        return soup.attrs['data-nm'], soup.attrs['data-cd'], soup.attrs['data-tp']

    def convert_code_to_name(self, item_code):
        # ER/PBR/배당수익률(개별종목) [12021] 을 위한 전종목 기본정보 [12005] 데이터
        request_data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01901',
            'mktId': '전체'
        }
        data = self.requests_data(request_data)
        for i in data[0]['OutBlock_1']:
            if i['ISU_SRT_CD'] == str(item_code):
                return i['ISU_ABBRV']


class ItemPrice(Stock):
    def __init__(self, code, start, end, day, division, item, **kwargs):
        """ 종목시세
        :param code: 항목 고유 번호
        :param start: 시작일
        :param end: 종료일
        :param day: 조회일자
        :param division: 시장구분
        """

        code_to_function = {
            '12001': self.price_of_entire_item,
            '12002': self.fluc_of_entire_item,
            '12003': self.trend_of_item_price,
            '12004': self.trend_of_item_price_by_month
        }

        super(ItemPrice, self).__init__(code, code_to_function, division, item, start, end, day, **kwargs)


    def price_of_entire_item(self):
        """ 전종목 시세 [12001] """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
            'mktId': self.division,
            'trdDd': self.day
        }
        return self.requests_data(data)

    def fluc_of_entire_item(self):
        """ 전종목 등락률 [12002] """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01602',
            'mktId': self.division,
            'strtDd': self.start,
            'endDd': self.end,
            'adjStkPrc_check': self.detail
        }
        return self.requests_data(data)

    def trend_of_item_price(self):
        """ 개별종목 시세 추이 [12003]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01701',
            'tboxisuCd_finder_stkisu0_2': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_tp,
            'codeNmisuCd_finder_stkisu0_2': self.data_nm,
            'param1isuCd_finder_stkisu0_2': 'STK',
            'strtDd': self.start,
            'endDd': self.end,
        }
        return self.requests_data(data)

    def trend_of_item_price_by_month(self):
        """ 개별종목 시세 추이 [12004]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01801',
            'tboxisuCd_finder_stkisu0_3': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_cd,
            'codeNmisuCd_finder_stkisu0_3': self.data_nm,
            'param1isuCd_finder_stkisu0_3': 'STK',
            'strtYy': self.start[:4],
            'strtMm': self.start[4:6],
            'endYy': self.end[:4],
            'endMm': self.end[:4:6],
            'strtYymm': self.start[:6],
            'endYymm': self.end[:6]
        }
        return self.requests_data(data)


class ItemInfo(Stock):
    def __init__(self, code, start, end, day, division):
        """ 종목시세
        :param code: 항목 고유 번호
        :param start: 시작일
        :param end: 종료일
        :param day: 조회일자
        :param division: 시장구분
        """

        code_to_function = {
            '12005': self.info_of_entire_itme,
            '12006': self.option_list_of_entire,
            '12007': 'Not Now',
        }

        super(ItemInfo, self).__init__(code, code_to_function, division, None, start, end, day)



    def info_of_entire_itme(self):
        """전체 종목 기본 정보 [12005]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01901',
            'mktId': self.division,
        }
        return self.requests_data(data)

    def option_list_of_entire(self):
        """전종목 지정 내역 [12006]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02001',
            'mktId': self.division
        }
        return self.requests_data(data)

    def total_info_of_stock(self):
        """ 개별종목 종합정보 [12007]"""
        pass


class TradePerform(Stock):
    def __init__(self, code, start, end, day, division, item, search_type, **kwargs):
        """ 종목시세
        :param code: 항목 고유 번호
        :param start: 시작일
        :param end: 종료일
        :param day: 조회일자
        :param division: 시장구분
        """
        code_to_function = {
            '12008': self.trade_perform_by_invastor,
            '12009': self.trade_perform_by_item,
            '12010': self.top_item_per_investor,
            '12011': self.block_trading_last_day,
            '12012': self.program_traing
        }

        super().__init__(code, code_to_function, division, item, start, end, day, **kwargs)
        self.search_type = search_type
        addition_item = kwargs.get('addition_item', None)
        if addition_item:
            addition_item = [item.upper() for item in addition_item]
        self.etf = 'ETF' if 'ETF' in addition_item else None
        self.etn = 'ETN' if 'ETN' in addition_item else None
        self.elw = 'ELW' if 'ELW' in addition_item else None


    def trade_perform_by_invastor(self):
        """투자자별 거래실적 [12008]"""
        # 기간합계(1)/일별추이(2)(inqTqCd) - 거래량(1)/거래대금(2)(trdValVol), 매도(1)/매수(2)/순매수(3)(askBid)
        # 기간합계는 detailView, trdValVol, askBid 가 없음.
        # KOSDAQ, KONEX는 ETF, ETN, ELW가 없음
        if self.search_type == '상세보기':
            bld = 'dbms/MDC/STAT/standard/MDCSTAT02203'
        elif self.detail == '일별추이':
            bld = 'dbms/MDC/STAT/standard/MDCSTAT02202'
        else:
            bld = 'dbms/MDC/STAT/standard/MDCSTAT02201'
        data = {
            'bld': bld,
            'inqTpCd': self.search_type,
            'trdVolVal': self.trade_index,
            'askBid': self.trade_check,
            'mktId': self.division,
            'etf': self.etf,
            'etn': self.etn,
            'elw': self.elw,
            'strtDd': self.start,
            'endDd': self.end,
            'detailView': self.detail,
        }
        return self.requests_data(data)

    def trade_perform_by_item(self):
        """투자자별 거래실적(개별종목) [12009]"""

        if self.detailView == '1':
            n = 3
        else:
            n = self.inqtpcd
        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0230{n}',
            'inqTpCd': self.inqtpcd,
            'trdVolVal': self.trdvolval,
            'askBid': self.askbid,
            'mktId': self.division,
            'tboxisuCd_finder_stkisu0_3': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_cd,
            'codeNmisuCd_finder_stkisu0_3': self.data_nm,
            'param1isuCd_finder_stkisu0_3': 'STK',
            'strtDd': self.start,
            'endDd': self.end,
            'detailView': self.detailView,
            'share': 2,
            'money': 3
        }
        return self.requests_data(data)

    def top_item_per_investor(self):
        """투자자별 순매수상위종목 [12010]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02401',
            'mktId': self.division,
            'invstTpCd': self.investor,
            'strtDd': self.start,
            'endDd': self.end,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def block_trading_last_day(self):
        """대량매매(전일) [12011]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02501',
            'mktId': self.division,
            'share': 1
        }
        return self.requests_data(data)

    def program_traing(self):
        """프로그램 매매 [12012]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02601',
            'mktId': self.division,
            'strtDd': self.start,
            'endDd': self.end,
            'share': 2,
            'money': 3
        }
        return self.requests_data(data)


class OtherSecurity(Stock):
    def __init__(self, code, start, end, day, division, item):

        code_to_function = {
            '12013': self.price_of_REITs,
            '12014': self.price_of_mutual_fund,
            '12015': self.price_of_ship_investor,
            '12016': self.price_of_infra_investor,
            '12017': self.price_of_certificate,
            '12018': self.price_of_warranty,
            '12019': self.price_of_subscription_warranty
        }

        super().__init__(code, code_to_function, division, item, start, end, day)

    def price_of_REITs(self):
        """REITs시세 [12013]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02701',
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def price_of_mutual_fund(self):
        """뮤추얼펀드 시세 [12014]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02801',
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def price_of_ship_investor(self):
        """선박투자회사 시세 [12015]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02901',
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def price_of_infra_investor(self):
        """인프라투융자회사 시세 [12016]"""
        data ={
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03001',
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def price_of_certificate(self):
        """수익증권 시세 [12017]"""
        data ={
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03101',
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def price_of_warranty(self):
        """신주인수권증권 시세 [12018]"""
        data ={
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03201',
            'mktId': self.division,
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def price_of_subscription_warranty(self):
        """신주인수권증서 시세 [12019]"""
        data ={
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03301',
            'mktId': self.division,
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)


class Detail(Stock):
    def __init__(self, code, start, end, day, division, item, **kwargs):

        code_to_function = {
            '12020': 'Not now',
            '12021': self.per_pbr_dividend_of_stock,
            '12022': self.holding_amount_of_foreigner,
            '12023': self.holding_amount_of_foreigner_by_item,
            '12024': self.distribution_per_business,
            '12025': self.stock_and_business_table,
            '12026': self.substitution_price_of_stock,
            '12027': self.substitution_price_of_beneficiary_certificate,
            '12028': self.substitution_price_of_mutual_fund

        }

        item_code = kwargs.get('item_code', None)
        super().__init__(code, start, end, day, division, item, item_code, code_to_function)
        search_type = kwargs.get('search_type', '전종목')
        isuLmtRto = kwargs.get('no_foreign_only', None)
        business = kwargs.get('business', None)

        # info.py 에서 input_to_value가 동작하는지 테스트 해본다
        self.search_type_test = kwargs.get('search_type', '전종목')
        self.isuLmtRto_test = kwargs.get('no_foreign_only', None)
        self.business_test = kwargs.get('business', None)
        print(self.business_test)
        ############################################

        self.company = kwargs.get('company', None)
        self.certificate = kwargs.get('certificate', None)

        self.search_type = self.search_type_to_number[search_type]
        self.isuLmRto = 1 if isuLmtRto is True else None
        if code in ['12024']:
            self.idxIndCd = business_to_number[business]




    def per_pbr_dividend_of_stock(self):
        """"PER/PBR/배당수익률(개별종목) [12021]"""
        if self.division == 'KONEX':
            raise Exception("No KONEX")
        n = self.search_type
        if n is 2: print(self.data_nm)
        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0350{n}',
            'searchType': n,
            'mktId': self.division,
            'trdDd': self.day,
            'tboxisuCd_finder_stkisu0_0': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_cd,
            'codeNmisuCd_finder_stkisu0_0': self.data_nm,
            'param1isuCd_finder_stkisu0_0': self.division,
            'strtDd': self.start,
            'endDd': self.end
        }
        ####### test ######
        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT03501',
            'searchType': self.search_type_test,
            'mktId': self.division,
            'trdDd': self.day,
            'tboxisuCd_finder_stkisu0_0': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_cd,
            'codeNmisuCd_finder_stkisu0_0': self.data_nm,
            'param1isuCd_finder_stkisu0_0': self.division,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def holding_amount_of_foreigner(self):
        """외국인보유량 추이 [12022]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03601',
            'mktId': self.division,
            'strtDd': self.start,
            'endDd': self.end,
            'share': 2,
            'money': 3
        }
        return self.requests_data(data)

    def holding_amount_of_foreigner_by_item(self):
        """외국인보유량(개별종목) [12023]"""
        n = self.search_type
        if n is 2:
            print(self.data_nm)
        print(self.isuLmRto)

        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0370{n}',
            'searchType': n,
            'mktId': self.division,
            'trdDd': self.day,
            'tboxisuCd_finder_stkisu0_0': f'{self.data_tp}/{self.data_nm}',
            'isuLmtRto': self.isuLmRto,
            'isuCd': self.data_cd,
            'isuCd2': self.data_cd,
            'codeNmisuCd_finder_stkisu0_0': self.data_nm,
            'param1isuCd_finder_stkisu0_0': 'STK', #self.division,
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def distribution_per_business(self):
        """
        업종별 분포 [12024]
        :arg
            [searchType = 1 (전종목)]
                search_type, day, division
            [searchType = 2 (개별추이)]
                search_type, division, business, start, end
        division in (KOSPI, KOSDAQ)
        """
        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0380{self.search_type}',
            'searchType': self.search_type,
            'mktId': self.division,
            'trdDd': self.day,
            'idxIndCd': self.idxIndCd,
            'strtDd': self.start,
            'endDd': self.end,
            'share': 2,
            'money': 3
        }

        #### test #####
        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT03801',
            'searchType': self.search_type_test,
            'mktId': self.division,
            'trdDd': self.day,
            'idxIndCd': self.business_test,
            'strtDd': self.start,
            'endDd': self.end,
            'share': 2,
            'money': 3
        }
        print(data)
        ##############################
        return self.requests_data(data)

    def stock_and_business_table(self):
        """
        업종분류 현황 [12025]
        :arg
            division, day
        division in (KOSPI, KOSDAQ)
        """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03901',
            'mktId': self.division,
            'trdDd': self.day,
            'money': 1
        }
        return self.requests_data(data)

    def substitution_price_of_stock(self):
        """
        주식 대용가 [12026]
        :arg
            [searchType = 1 (전종목)]
                search_type, day, division
            [searchType = 2 (개별추이)]
                search_type, dividion, business, start, end
        """
        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0400{self.search_type}',
            'searchType': self.search_type,
            'mktId': self.division,
            'trdDd': self.day,
            'tboxisuCd_finder_stkisu0_1': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_tp,
            'codeNmisuCd_finder_stkisu0_1': self.data_nm,
            'param1isuCd_finder_stkisu0_1': 'STK',
            'strtDd': self.start,
            'endDd': self.end
        }
        ######### test ##########

        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT04001',
            'searchType': self.search_type_test,
            'mktId': self.division,
            'trdDd': self.day,
            'tboxisuCd_finder_stkisu0_1': f'{self.data_tp}/{self.data_nm}',
            'isuCd': self.data_cd,
            'isuCd2': self.data_tp,
            'codeNmisuCd_finder_stkisu0_1': self.data_nm,
            'param1isuCd_finder_stkisu0_1': 'STK',
            'strtDd': self.start,
            'endDd': self.end
        }

        return self.requests_data(data)

    def substitution_price_of_beneficiary_certificate(self):
        """
        수익증권 대용가 [12027]
        :arg
            [searchType = 1 (전종목)]
                search_type, day, division
            [searchType = 2 (개별추이)]
                search_type, start, end, company, certificate
        """
        if self.search_type == 1:
            strtYy = self.day[:4]
            strtMm = self.day[4:6]
        else:
            strtYy = self.start[:4]
            strtMm = self.start[4:6]
        endYy = self.end[:4]
        endMm = self.end[4:6]

        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0410{self.search_type}',
            'strtYy': strtYy,
            'strtMm': strtMm,
            'searchType': self.search_type,
            'comNm': self.company,
            'isuNm': self.certificate,
            'endYy': endYy,
            'endMm': endMm
        }

        return self.requests_data(data)

    def substitution_price_of_mutual_fund(self):
        """
        뮤추얼펀드 대용가 [12028]
        :arg
            [searchType = 1 (전종목)]
                search_type, day, division
            [searchType = 2 (개별추이)]
                search_type, start, end, company, certificate
        """
        if self.search_type == 1:
            strtYy = self.day[:4]
            strtMm = self.day[4:6]
        else:
            strtYy = self.start[:4]
            strtMm = self.start[4:6]
        endYy = self.end[:4]
        endMm = self.end[4:6]

        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0420{self.search_type}',
            'strtYy': strtYy,
            'strtMm': strtMm,
            'searchType': self.search_type,
            'comNm': self.company,
            'isuNm': self.certificate,
            'endYy': endYy,
            'endMm': endMm
        }

        return self.requests_data(data)
