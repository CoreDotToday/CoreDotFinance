# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from finance.statistics.basic.info import Info

class Stock(Info):
    def __init__(self, code, start, end, day, division, stk_name, code_to_function):
        """
        주가
        :param code:
        :param start:
        :param end:
        :param day:
        :param division:
        :param stk_name:
        """
        super(Stock, self).__init__(code, start, end, day)

        self.division_category = {
            '전체': 'ALL',
            'KOSPI': 'STK',
            'KOSDAQ': 'KSQ',
            'KONEX': 'KNX'
        }

        self.item_name, self.isuCd, self.isuCd2 = self._find_stock_data(stk_name)
        self.division = '전체' if division is None else division.upper()
        self.function = code_to_function[code]


    def _find_stock_data(self, stk_name):
        if stk_name is None:
            stk_name = '삼성전자'
        stock_autocomplete_url = 'http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_stkisu&value={value}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_stkisu_autocomplete'
        response = requests.get(stock_autocomplete_url.format(value=stk_name))
        soup = bs(response.content, 'html.parser').li

        if soup is None:
            raise AttributeError(f'{stk_name} is Wrong name as an stock name')

        item_name = soup.attrs['data-nm']
        isuCd = soup.attrs['data-cd'] #data-cd='KR7333430007'
        isuCd2 = soup.attrs['data-tp'] #data-tp='307070'

        return item_name, isuCd, isuCd2


class ItemPrice(Stock):
    def __init__(self, code, start, end, day, division, adj_price, stk_name):
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

        self.adj_stk_prc = {
            True: 2,
            False: 1
        }

        super(ItemPrice, self).__init__(code, start, end, day, division, stk_name, code_to_function)
        self.adj_price = adj_price



    def price_of_entire_item(self):
        """ 전종목 시세 [12001] """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
            'mktId': self.division_category[self.division],
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def fluc_of_entire_item(self):
        """ 전종목 등락률 [12002] """
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01602',
            'mktId': self.division_category[self.division],
            'strtDd': self.start,
            'endDd': self.end,
            'adjStkPrc': self.adj_stk_prc[self.adj_price],
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def trend_of_item_price(self):
        """ 개별종목 시세 추이 [12003]"""
        print(self.isuCd2, '-', self.item_name)
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01701',
            'tboxisuCd_finder_stkisu0_2': f'{self.isuCd2}/{self.item_name}',
            'isuCd': self.isuCd,
            'isuCd2': self.isuCd2,
            'codeNmisuCd_finder_stkisu0_2': self.item_name,
            'param1isuCd_finder_stkisu0_2': 'STK',
            'strtDd': self.start,
            'endDd': self.end,
            'share': 1,
            'money': 1
        }
        return self.requests_data(data)

    def trend_of_item_price_by_month(self):
        """ 개별종목 시세 추이 [12004]"""
        print(self.isuCd2, '-', self.item_name)
        srt = str(self.start)
        end = str(self.end)
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01801',
            'tboxisuCd_finder_stkisu0_3': f'{self.isuCd2}/{self.item_name}',
            'isuCd': self.isuCd,
            'isuCd2': self.isuCd,
            'codeNmisuCd_finder_stkisu0_3': self.item_name,
            'param1isuCd_finder_stkisu0_3': 'STK',
            'strtYy': srt[:4],
            'strtMm': srt[4:6],
            'endYy': end[:4],
            'endMm': end[:4:6],
            'strtYymm': srt[:6],
            'endYymm': end[:6],
            'share': 1,
            'money': 1
        }
        return self.requests_data(data)


class ItemInfo(Stock):
    def __init__(self, code, start, end, day, division, stk_name):
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

        super(ItemInfo, self).__init__(code, start, end, day, division, stk_name, code_to_function)



    def info_of_entire_itme(self):
        """전체 종목 기본 정보 [12005]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01901',
            'mktId': self.division_category[self.division],
            'share': 1
        }
        return self.requests_data(data)

    def option_list_of_entire(self):
        """전종목 지정 내역 [12006]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02001',
            'mktId': self.division_category[self.division]
        }
        return self.requests_data(data)

    def total_info_of_stock(self):
        """ 개별종목 종합정보"""
        pass


class TradePerform(Stock):
    def __init__(self, code, start, end, day, division, stk_name, options, investor, **trd):
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

        investor_to_code = {
            '금융투자': 1000,
            '보험': 2000,
            '투신': 3000,
            '사모': 3100,
            '은행': 4000,
            '기타금융': 5000,
            '연기금 등': 6000,
            '기관합계': 7050,
            '기타법인': 7100,
            '개인': 8000,
            '외국인': 9000,
            '기타외국인': 9001,
            '전체': 9999
        }
        super().__init__(code, start, end, day, division, stk_name, code_to_function)
        self.investor = investor_to_code['전체'] if investor is None else investor_to_code[investor]
        self.etf, self.etn, self.elw, self.detailView = self.sort_options(options)
        if code in ['12008', '12009']:
            self.inqtpcd, self.trdvolval, self.askbid = self.sort_trd(**trd)


    def sort_options(self, option):
        option = [o.upper() for o in option]
        lis = []
        if 'ETF' in option:
            lis.append('EF')
        else:
            lis.append('')
        if 'ETN' in option:
            lis.append('EN')
        else:
            lis.append('')
        if 'ELW' in option:
            lis.append('EW')
        else:
            lis.append('')
        if 'DETAIL' in option:
            lis.append('1')
        else:
            lis.append('')
        return lis

    def sort_trd(self, **trd):
        inqtpcd = trd.get('inqtpcd', None)
        if inqtpcd == '기간합계':
            inqtpcd = 1
            return inqtpcd, None, None
        elif inqtpcd == '일별추이':
            inqtpcd = 2
        else:
            raise Exception(f'Wrong input: \'{inqtpcd}\'. '
                            f'\'inqtpcd\' should be one of \'기간합계\', \'일별추이\'')
        trdvalvol = trd.get('trdvolval', None)
        if trdvalvol == '거래량':
            trdvalvol = 1
        elif trdvalvol == '거래대금':
            trdvalvol = 2
        else:
            raise Exception(f'Wrong input: \'{trdvalvol}\'. '
                            f'\'trdvolval\' should be one of \'거래량\', \'거래대금\'')
        askbid = trd.get('askbid', None)
        if askbid == '매도':
            askbid = 1
        elif askbid == '매수':
            askbid = 2
        elif askbid == '순매수':
            askbid = 3
        else:
            raise Exception(f'Wrong input: \'{askbid}\'. '
                            f'\'askbid\' should be one of \'매도\', \'매수\', \'순매수\'')
        return inqtpcd, trdvalvol, askbid


    def trade_perform_by_invastor(self):
        """투자자별 거래실적 [12008]"""
        # 기간합계(1)/일별추이(2)(inqTqCd) - 거래량(1)/거래대금(2)(trdValVol), 매도(1)/매수(2)/순매수(3)(askBid)
        # 기간합계는 detailView, trdValVol, askBid 가 없음.
        # KOSDAQ, KONEX는 ETF, ETN, ELW가 없음
        if self.detailView == '1':
            n = 3
        else:
            n = self.inqtpcd
        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0220{n}',
            'inqTpCd': self.inqtpcd,
            'trdVolVal': self.trdvolval,
            'askBid': self.askbid,
            'mktId': self.division_category[self.division],
            'etf': self.etf,
            'etn': self.etn,
            'elw': self.elw,
            'strtDd': self.start,
            'endDd': self.end,
            'detailView': self.detailView,
            'share': 2,
            'money': 3
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
            'mktId': self.division_category[self.division],
            'tboxisuCd_finder_stkisu0_3': f'{self.isuCd2}/{self.item_name}',
            'isuCd': self.isuCd,
            'isuCd2': self.isuCd,
            'codeNmisuCd_finder_stkisu0_3': self.item_name,
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
            'mktId': self.division_category[self.division],
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
            'mktId': self.division_category[self.division],
            'share': 1
        }
        return self.requests_data(data)

    def program_traing(self):
        """프로그램 매매 [12012]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT02601',
            'mktId': self.division_category[self.division],
            'strtDd': self.start,
            'endDd': self.end,
            'share': 2,
            'money': 3
        }
        return self.requests_data(data)

class OtherSecurity(Stock):
    def __init__(self, code, start, end, day, division, stk_name):

        code_to_function = {
            '12013': self.price_of_REITs,
            '12014': self.price_of_mutual_fund,
            '12015': self.price_of_ship_investor,
            '12016': self.price_of_infra_investor,
            '12017': self.price_of_certificate,
            '12018': self.price_of_warranty,
            '12019': self.price_of_subscription_warranty
        }

        super().__init__(code, start, end, day, division, stk_name, code_to_function)

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
            'mktId': self.division_category[self.division],
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

    def price_of_subscription_warranty(self):
        """신주인수권증서 시세 [12019]"""
        data ={
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03301',
            'mktId': self.division_category[self.division],
            'trdDd': self.day,
            'share': 1,
            'money': 1,
        }
        return self.requests_data(data)

class Detail(Stock):
    def __init__(self, code, start, end, day, division, stk_name, **kwargs):

        code_to_function = {
            '12020': 'Not now',
            '12021': self.per_pbr_dividend_of_stock,
            '12022': self.holding_amount_of_foreigner,
            '12023': self.holding_amount_of_foreigner_by_item
        }
        search_type_to_number = {
            '전종목': 1,
            '개별추이': 2
        }
        super().__init__(code, start, end, day, division, stk_name, code_to_function)
        search_type = kwargs.get('search_type', '전종목')
        isuLmtRto = kwargs.get('no_foreign_only', None)
        self.isuLmRto = 1 if isuLmtRto is True else None
        self.search_type = search_type_to_number[search_type]

    def per_pbr_dividend_of_stock(self):
        """"PER/PBR/배당수익률(개별종목) [12021]"""
        if self.division == 'KONEX':
            raise Exception("No KONEX")
        n = self.search_type
        if n is 2: print(self.item_name)
        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0350{n}',
            'searchType': n,
            'mktId': self.division_category[self.division],
            'trdDd': self.day,
            'tboxisuCd_finder_stkisu0_0': f'{self.isuCd2}/{self.item_name}',
            'isuCd': self.isuCd,
            'isuCd2': self.isuCd,
            'codeNmisuCd_finder_stkisu0_0': self.item_name,
            'param1isuCd_finder_stkisu0_0': self.division_category[self.division],
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)

    def holding_amount_of_foreigner(self):
        """외국인보유량 추이 [12022]"""
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT03601',
            'mktId': self.division_category[self.division],
            'strtDd': 20210126,
            'endDd': 20210202,
            'share': 2,
            'money': 3
        }
        return self.requests_data(data)

    def holding_amount_of_foreigner_by_item(self):
        """외국인보유량(개별종목) [12023]"""
        n = self.search_type
        if n is 2: print(self.item_name)
        print(self.isuLmRto)

        data = {
            'bld': f'dbms/MDC/STAT/standard/MDCSTAT0370{n}',
            'searchType': n,
            'mktId': self.division_category[self.division],
            'trdDd': self.day,
            'tboxisuCd_finder_stkisu0_0': f'{self.isuCd2}/{self.item_name}',
            'isuLmtRto': self.isuLmRto,
            'isuCd': self.isuCd,
            'isuCd2': self.isuCd,
            'codeNmisuCd_finder_stkisu0_0': self.item_name,
            'param1isuCd_finder_stkisu0_0': self.division_category[self.division],
            'strtDd': self.start,
            'endDd': self.end
        }
        return self.requests_data(data)