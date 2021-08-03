# -*- coding: utf-8 -*-
from coredotfinance.krx.core.krx_website.info import Info


class Stock(Info):
    def __init__(self, code, start, end, date, symbol, **kwargs):
        """
        주가
        :param code:
        :param start:
        :param end, 'index':
        :param day:
        :param division:
        :param item:
        """
        self.code = code
        self.start = start
        self.end = end
        self.date = date
        self.symbol = symbol
        self.detail = kwargs.get("detail", None)
        self.trade_index = kwargs.get("trade_index", None)
        self.trade_check = kwargs.get("trade_check", None)
        self.search_type = kwargs.get("search_type", None)
        self.investor = kwargs.get("investor", None)
        self.inquiry = kwargs.get("inquiry", None)
        self.search_type = kwargs.get("search_type", "전종목")
        self.sort_type = kwargs.get("sort_type", "종목명")
        self.isuLmtRto = kwargs.get("no_foreign_only", None)
        self.business = kwargs.get("business", None)
        self.company = kwargs.get("company", None)

        addition_item = kwargs.get("addition_item", None)
        if addition_item:
            addition_item = [item.upper() for item in addition_item]
            self.etf = "ETF" if "ETF" in addition_item else None
            self.etn = "ETN" if "ETN" in addition_item else None
            self.elw = "ELW" if "ELW" in addition_item else None

        if symbol:
            self.data_nm, self.data_cd, self.data_tp = self.autocomplete(
                symbol, "stock"
            )
        division = kwargs.get("division", None)
        self.division = "전체" if division is None else division.upper()

        self.code_to_function = {
            "12001": self.price_of_entire_item,
            "12002": self.fluc_of_entire_item,
            "12003": self.trend_of_item_price,
            "12004": self.trend_of_item_price_by_month,
            "12005": self.info_of_entire_itme,
            "12006": self.option_list_of_entire,
            "12007": "Not Now",
            "12008": self.trade_perform_by_invastor,
            "12009": self.trade_perform_by_item,
            "12010": self.top_item_per_investor,
            "12011": self.block_trading_last_day,
            "12012": self.program_traing,
            "12013": self.price_of_REITs,
            "12014": self.price_of_mutual_fund,
            "12015": self.price_of_ship_investor,
            "12016": self.price_of_infra_investor,
            "12017": self.price_of_certificate,
            "12018": self.price_of_warranty,
            "12019": self.price_of_subscription_warranty,
            "12020": self.detail_search_of_listed_company,
            "12021": self.per_pbr_dividend_of_stock,
            "12022": self.holding_amount_of_foreigner,
            "12023": self.holding_amount_of_foreigner_by_item,
            "12024": self.distribution_per_business,
            "12025": self.stock_and_business_table,
            "12026": self.substitution_price_of_stock,
            "12027": self.substitution_price_of_beneficiary_certificate,
            "12028": self.substitution_price_of_mutual_fund,
        }
        self.get_requested_data = self.code_to_function[code]

    def price_of_entire_item(self):
        """전종목 시세 [12001]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01501",
            "mktId": self.division,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def fluc_of_entire_item(self):
        """전종목 등락률 [12002]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01602",
            "mktId": self.division,
            "strtDd": self.start,
            "endDd": self.end,
            "adjStkPrc_check": self.detail,
        }
        return self.update_requested_data(data)

    def trend_of_item_price(self):
        """개별종목 시세 추이 [12003]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01701",
            "tboxisuCd_finder_stkisu0_2": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_tp,
            "codeNmisuCd_finder_stkisu0_2": self.data_nm,
            "param1isuCd_finder_stkisu0_2": "STK",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def trend_of_item_price_by_month(self):
        """개별종목 시세 추이 [12004]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01801",
            "tboxisuCd_finder_stkisu0_3": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_cd,
            "codeNmisuCd_finder_stkisu0_3": self.data_nm,
            "param1isuCd_finder_stkisu0_3": "STK",
            "strtYy": self.start[:4],
            "strtMm": self.start[4:6],
            "endYy": self.end[:4],
            "endMm": self.end[:4:6],
            "strtYymm": self.start[:6],
            "endYymm": self.end[:6],
        }
        return self.update_requested_data(data)

    def info_of_entire_itme(self):
        """전체 종목 기본 정보 [12005]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01901",
            "mktId": self.division,
        }
        return self.update_requested_data(data)

    def option_list_of_entire(self):
        """전종목 지정 내역 [12006]"""
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT02001", "mktId": self.division}
        return self.update_requested_data(data)

    def total_info_of_stock(self):
        """개별종목 종합정보 [12007]"""
        pass

    def trade_perform_by_invastor(self):
        """투자자별 거래실적 [12008]"""
        # 기간합계(1)/일별추이(2)(inqTqCd) - 거래량(1)/거래대금(2)(trdValVol), 매도(1)/매수(2)/순매수(3)(askBid)
        # 기간합계는 detailView, trdValVol, askBid 가 없음.
        # KOSDAQ, KONEX는 ETF, ETN, ELW가 없음
        if self.detail == "상세보기":
            bld = "dbms/MDC/STAT/standard/MDCSTAT02203"
        elif self.search_type == "일별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT02202"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT02201"
        data = {
            "bld": bld,
            "inqTpCd": self.search_type,
            "trdVolVal": self.trade_index,
            "askBid": self.trade_check,
            "mktId": self.division,
            "etf": self.etf,
            "etn": self.etn,
            "elw": self.elw,
            "strtDd": self.start,
            "endDd": self.end,
            "detailView": self.detail,
        }
        return self.update_requested_data(data)

    def trade_perform_by_item(self):
        """투자자별 거래실적(개별종목) [12009]"""
        if self.detail == "상세보기":
            bld = "dbms/MDC/STAT/standard/MDCSTAT02303"
        elif self.search_type == "일별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT02302"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT02301"
        data = {
            "bld": bld,
            "inqTpCd": self.search_type,
            "trdVolVal": self.trade_index,
            "askBid": self.trade_check,
            "tboxisuCd_finder_stkisu0_3": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_cd,
            "codeNmisuCd_finder_stkisu0_3": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
            "detailView": self.detail,
        }
        return self.update_requested_data(data)

    def top_item_per_investor(self):
        """투자자별 순매수상위종목 [12010]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT02401",
            "mktId": self.division,
            "invstTpCd": self.investor,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def block_trading_last_day(self):
        """대량매매(전일) [12011]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT02501",
            "mktId": self.division,
        }
        return self.update_requested_data(data)

    def program_traing(self):
        """프로그램 매매 [12012]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT02601",
            "mktId": self.division,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def price_of_REITs(self):
        """REITs시세 [12013]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT02701",
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def price_of_mutual_fund(self):
        """뮤추얼펀드 시세 [12014]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT02801",
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def price_of_ship_investor(self):
        """선박투자회사 시세 [12015]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT02901",
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def price_of_infra_investor(self):
        """인프라투융자회사 시세 [12016]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT03001",
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def price_of_certificate(self):
        """수익증권 시세 [12017]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT03101",
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def price_of_warranty(self):
        """신주인수권증권 시세 [12018]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT03201",
            "mktId": self.division,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def price_of_subscription_warranty(self):
        """신주인수권증서 시세 [12019]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT03301",
            "mktId": self.division,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def detail_search_of_listed_company(self):
        """상장회사 상세검색 [12020]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT03402",
            "mktTpCd": self.division,
            "tboxisuSrtCd_finder_listisu0_3": f"{self.data_tp}/{self.data_nm}",
            "isuSrtCd": self.data_cd,
            "isuSrtCd2": "A" + self.data_tp,
            "codeNmisuSrtCd_finder_listisu0_3": self.data_nm,
            "sortType": self.sort_type,
        }
        return self.update_requested_data(data)

    def per_pbr_dividend_of_stock(self):
        """ "PER/PBR/배당수익률(개별종목) [12021]"""
        if self.search_type == "개별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT03502"
        else:
            self.data_nm, self.data_cd, self.data_tp = None, None, None
            bld = "dbms/MDC/STAT/standard/MDCSTAT03501"

        data = {
            "bld": bld,
            "searchType": self.search_type,
            "mktId": self.division,
            "trdDd": self.date,
            "tboxisuCd_finder_stkisu0_0": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_cd,
            "codeNmisuCd_finder_stkisu0_0": self.data_nm,
            "param1isuCd_finder_stkisu0_0": self.division,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def holding_amount_of_foreigner(self):
        """외국인보유량 추이 [12022]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT03601",
            "mktId": self.division,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def holding_amount_of_foreigner_by_item(self):
        """외국인보유량(개별종목) [12023]"""
        if self.search_type == "개별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT03702"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT03701"

        data = {
            "bld": bld,
            "searchType": self.search_type,
            "mktId": self.division,
            "trdDd": self.date,
            "tboxisuCd_finder_stkisu0_0": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_cd,
            "codeNmisuCd_finder_stkisu0_0": self.data_nm,
            "param1isuCd_finder_stkisu0_0": self.division,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

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
        if self.search_type == "개별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT03802"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT03801"

        data = {
            "bld": bld,
            "searchType": self.search_type,
            "mktId": self.division,
            "trdDd": self.date,
            "idxIndCd": self.inquiry,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def stock_and_business_table(self):
        """
        업종분류 현황 [12025]
        :arg
            division, day
        division in (KOSPI, KOSDAQ)
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT03901",
            "mktId": self.division,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def substitution_price_of_stock(self):
        """
        주식 대용가 [12026]
        :arg
            [searchType = 1 (전종목)]
                search_type, day, division
            [searchType = 2 (개별추이)]
                search_type, dividion, business, start, end
        """
        if self.search_type == "개별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT04002"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT04001"
        data = {
            "bld": bld,
            "searchType": self.search_type,
            "mktId": self.division,
            "trdDd": self.date,
            "tboxisuCd_finder_stkisu0_1": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_tp,
            "codeNmisuCd_finder_stkisu0_1": self.data_nm,
            "param1isuCd_finder_stkisu0_1": "STK",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def substitution_price_of_beneficiary_certificate(self):
        """
        수익증권 대용가 [12027]
        :arg
            [searchType = 1 (전종목)]
                search_type, day, division
            [searchType = 2 (개별추이)]
                search_type, start, end, company, certificate
        """
        if self.search_type == "전종목":
            strtYy = self.date[:4]
            strtMm = self.date[4:6]
            bld = "dbms/MDC/STAT/standard/MDCSTAT04101"
        else:
            strtYy = self.start[:4]
            strtMm = self.start[4:6]
            bld = "dbms/MDC/STAT/standard/MDCSTAT04102"
        endYy = self.end[:4]
        endMm = self.end[4:6]

        data = {
            "bld": bld,
            "strtYy": strtYy,
            "strtMm": strtMm,
            "searchType": self.search_type,
            "comNm": self.company,
            "isuNm": self.item,
            "endYy": endYy,
            "endMm": endMm,
        }

        return self.update_requested_data(data)

    def substitution_price_of_mutual_fund(self):
        """
        뮤추얼펀드 대용가 [12028]
        :arg
            [searchType = 1 (전종목)]
                search_type, day, division
            [searchType = 2 (개별추이)]
                search_type, start, end, company, certificate
        """
        if self.search_type == "전종목":
            strtYy = self.date[:4]
            strtMm = self.date[4:6]
            bld = "dbms/MDC/STAT/standard/MDCSTAT04201"
        else:
            strtYy = self.start[:4]
            strtMm = self.start[4:6]
            bld = "dbms/MDC/STAT/standard/MDCSTAT04202"
        endYy = self.end[:4]
        endMm = self.end[4:6]

        data = {
            "bld": bld,
            "strtYy": strtYy,
            "strtMm": strtMm,
            "searchType": self.search_type,
            "comNm": self.company,
            "isuNm": self.item,
            "endYy": endYy,
            "endMm": endMm,
        }

        return self.update_requested_data(data)
