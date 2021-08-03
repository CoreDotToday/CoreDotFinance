# -*- coding: utf-8 -*-
from coredotfinance.krx.core.krx_website.info import Info


class Product(Info):
    def __init__(self, code, symbol, start, end, date, **kwargs):
        """
        증권상품
        :param code:
        :param start:
        :param end:
        :param day:
        :param product:
        :param code_to_function:
        """
        self.code = code
        self.start = start
        self.end = end
        self.date = date
        self.symbol = symbol

        if symbol:
            self.data_nm, self.data_cd, self.data_tp = self.autocomplete(
                symbol, "etf"
            )
        self.search_type = kwargs.get("search_type", None)
        self.trade_index = kwargs.get("trade_index", None)
        self.trade_check = kwargs.get("trade_check", None)
        self.quarter = kwargs.get("quarter", None)
        self.issuing = kwargs.get("issuing", None)
        self.basic_asset = kwargs.get("basic_asset", None)

        code_to_function = {
            "13101": self.etf_price_of_entire_items,
            "13102": self.etf_fluc_of_entire_items,
            "13103": self.etf_price_trend_of_item,
            "13104": self.etf_info_of_entire_items,
            "13105": self.etf_info_of_item,
            "13106": self.etf_trade_performance_per_investor,
            "13107": self.etf_trade_performance_per_investor_item,
            "13108": self.etf_portfolio_deposit_file,
            "13109": self.detail_of_ETF,
            "13110": self.result_of_active_ETF,
            "13111": "not now",
            "13112": self.etf_trend_of_tracking_error,
            "13113": self.etf_trend_of_differential,
            "13114": self.etf_trend_of_closing_differential,
            "13115": self.risk_of_multi_ETF_trader,
            "13116": self.managing_index_and_security_of_multi_ETF,
            "13117": self.etf_assessment_of_LP_per_quarter,
            "13201": self.etn_price_of_entire_items,
            "13202": self.etn_fluc_of_entire_items,
            "13203": self.etn_price_trend_of_item,
            "13204": self.etn_info_of_entire_items,
            "13205": self.etn_info_of_item,
            "13206": self.etn_trade_performance_per_investor,
            "13207": self.etn_trade_performance_per_investor_item,
            "13208": self.detail_of_ETN,
            "13209": self.etn_product_consisting_of_index,
            "13210": self.etn_credit_and_NCR,
            "13211": self.etn_risk_of_credit,
            "13212": self.condition_of_early_repayment_loss_limited_ETN,
            "13213": self.consideration_of_range_accurual_of_loss_limited_ETN,
            "13214": self.etn_trend_of_differential,
            "13215": self.etn_trend_of_closing_differential,
            "13301": self.elw_price_of_entire_items,
            "13302": self.elw_trend_of_item,
            "13303": self.elw_info_of_entire_items,
            "13304": self.elw_entire_info_of_item,
            "13305": self.elw_trade_performance_per_investor,
            "13306": self.elw_trade_performance_per_basic_asset,
            "13307": self.elw_item_of_residual_expiration_status,
            "13308": self.elw_item_of_beneficial_expiration_status,
            "13309": self.elw_approach_level_of_early_close,
            "13310": self.elw_log_of_early_close,
            "13311": self.elw_status_of_floating_per_basic_asset,
            "13312": self.elw_status_of_floating_per_issuing,
            "13313": self.elw_assessment_of_LP_per_quarter,
        }

        self.get_requested_data = code_to_function[code]

    def etf_price_of_entire_items(self):
        """
        전종목 시세[13101]
        :arg
            day
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT04301",
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def etf_fluc_of_entire_items(self):
        """
        전종목 등락률[13102]
        :arg
            start, end
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT04401",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def etf_price_trend_of_item(self):
        """
        개별종목 시세 추이[13103]
        :arg
            product, start, end
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT04501",
            "tboxisuCd_finder_secuprodisu1_31": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_cd,
            "codeNmisuCd_finder_secuprodisu1_31": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def etf_info_of_entire_items(self):
        """전종목 기본정보[13104]"""
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT04601", "share": 1}
        return self.update_requested_data(data)

    def etf_info_of_item(self):
        """개별종목 종합정보[13105]"""
        """Not now"""
        pass

    def etf_trade_performance_per_investor(self):
        """
        투자자별 거래실적 [13106]
        :arg
            search_type, trade_index, trade, start, end
        """
        if self.search_type == "일별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT04802"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT04801"
        data = {
            "bld": bld,
            "inqTpCd": self.search_type,
            "inqCondTpCd1": self.trade_index,
            "inqCondTpCd2": self.trade_check,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def etf_trade_performance_per_investor_item(self):
        """
        투자자별 거래실적(개별종목) [13107]
        :arg
            search_type, trade_index, trade, product, start, end
        """
        if self.search_type == "일별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT04902"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT04901"
        data = {
            "bld": bld,
            "inqTpCd": self.search_type,
            "inqCondTpCd1": self.trade_index,
            "inqCondTpCd2": self.trade_check,
            "tboxisuCd_finder_secuprodisu1_4": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_cd,
            "codeNmisuCd_finder_secuprodisu1_4": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def etf_portfolio_deposit_file(self):
        """
        PDF (Porrfolio Deposit File) [13108]
        :arg
            product, day
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT05001",
            "tboxisuCd_finder_secuprodisu1_6": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_cd,
            "codeNmisuCd_finder_secuprodisu1_6": self.data_nm,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def detail_of_ETF(self):
        """
        ETF 상세검색 [13109]
        Not now
        """
        pass

    def result_of_active_ETF(self):
        """
        액티브 ETF 실적 [13110]
        search_type, product, start, end
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT05701",
            "cls": self.search_type,
            "isuCd": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def incorporated_asset_of_active_ETF(self):
        """
        액티브ETF 편입자산현황 [13111]
        :arg
            day, product, search_type
        """
        if self.search_type == "잔존만기":
            bld = "dbms/MDC/STAT/standard/MDCSTAT05801"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT05802"
        year = self.date[:4]
        month = self.date[4:6]
        data = {
            "bld": bld,
            "isuCd": self.data_nm,
            "startYear": year,
            "startMonth": month,
        }
        return self.update_requested_data(data)

    def etf_trend_of_tracking_error(self):
        """
        추적오차율 추이 [13112]
        :arg
            product, start, end
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT05901",
            "isuCd": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def etf_trend_of_differential(self):
        """
        괴리율 추이 [13113]
        :arg
            product, start, end
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT06001",
            "isuCd": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def etf_trend_of_closing_differential(self):
        """
        장마감 괴리율 추이 [13114]
        :arg
            product, start, end
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT17101",
            "isuCd": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }

        return self.update_requested_data(data)

    def risk_of_multi_ETF_trader(self):
        """
        합성ETF 거래상대방 위험 [13115]
        :arg
            product, search_type
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT06101",
            "cls": self.search_type,
            "isuCd": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def managing_index_and_security_of_multi_ETF(self):
        """
        합성ETF 기초지수 및 담보관리[13116]
        """
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT06201"}
        return self.update_requested_data(data)

    def etf_assessment_of_LP_per_quarter(self):
        """분기별 LP 평가[]13117"""
        year = self.date[:4]
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT06301",
            "year": year,
            "quarter": self.quarter,
        }
        return self.update_requested_data(data)

    def etn_price_of_entire_items(self):
        """
        전종목 시세 [13201]
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT06401",
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def etn_fluc_of_entire_items(self):
        """
        전종목 등락률 [13202]
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT06501",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def etn_price_trend_of_item(self):
        """
        개별종목 시세추이 [13203]
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT06601",
            "tboxisuCd_finder_secuprodisu2_5": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "codeNmisuCd_finder_secuprodisu2_5": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def etn_info_of_entire_items(self):
        """
        전종목 기본정보 [13204]
        """
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT06701"}
        return self.update_requested_data(data)

    def etn_info_of_item(self):
        """
        개별종목 종합정보 [13205]
        not now
        """
        pass

    def etn_trade_performance_per_investor(self):
        """
        투자자별 거래실적 [13206]
        """
        if self.search_type == "일별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT06902"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT06901"

        data = {
            "bld": bld,
            "inqTpCd": self.search_type,
            "inqCondTpCd1": self.trade_index,
            "inqCondTpCd2": self.trade_check,
            "strtDd": self.start,
            "endDd": self.end,
        }

        return self.update_requested_data(data)

    def etn_trade_performance_per_investor_item(self):
        """
        투자자별 거래실적(개별종목) [13207]
        """
        if self.search_type == "일별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT07002"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT07001"

        data = {
            "bld": bld,
            "inqTpCd": self.search_type,
            "inqCondTpCd1": self.trade_index,
            "inqCondTpCd2": self.trade_check,
            "tboxisuCd_finder_secuprodisu2_10": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "codeNmisuCd_finder_secuprodisu2_10": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def detail_of_ETN(self):
        """
        ETN 상세검색 [13208]
        not now
        """
        pass

    def etn_product_consisting_of_index(self):
        """
        기초지수 구성요소 [13209]
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT07601",
            "tboxisuCd_finder_secuprodisu2_2": self.data_nm,
            "isuCd": self.data_cd,
            "isuCd2": self.data_tp,
            "codeNmisuCd_finder_secuprodisu2_2": self.data_nm,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def etn_credit_and_NCR(self):
        """
        발행사 신용등급 및 NCR [13210]
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT07701",
            "tboxisuCd_finder_secuprodisu2_3": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "codeNmisuCd_finder_secuprodisu2_3": self.data_nm,
        }
        return self.update_requested_data(data)

    def etn_risk_of_credit(self):
        """
        발행사 신용위험지표 [13211]
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT07801",
            "isurCd": self.issuing,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def condition_of_early_repayment_loss_limited_ETN(self):
        """
        손실제한ETN 조기상환 조건 [13212]
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT07901",
            "isuCd": self.data_cd,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def consideration_of_range_accurual_of_loss_limited_ETN(self):
        """
        손실제한ETN 레인지어쿠루얼 참고사항 [13213]
        No data!!
        """
        pass

    def etn_trend_of_differential(self):
        """
        괴리율 추이 [13214]
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT08101",
            "isuCd": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def etn_trend_of_closing_differential(self):
        """
        장마감 괴리율 추이 [13215]
        """
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT17201",
            "isuCd": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def etn_assessment_of_LP_per_quarter(self):
        """분기별 LP 평가 [13216]"""
        """Web page error """

    def elw_price_of_entire_items(self):
        """전종목 시세[13301]"""
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT08301", "trdDd": self.date}
        return self.update_requested_data(data)

    def elw_trend_of_item(self):
        """개별종목 시세 추이[13302]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT08401",
            "tboxisuCd_finder_secuprodisu3_34": f"{self.data_tp}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_tp,
            "codeNmisuCd_finder_secuprodisu3_34": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def elw_info_of_entire_items(self):
        """전종목 기본정보[13303]"""
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT08501"}
        return self.update_requested_data(data)

    def elw_entire_info_of_item(self):
        """개별종목 종합정보[13304]
        Not now"""
        pass

    def elw_trade_performance_per_investor(self):
        """투자자별 거래실적[13305]"""
        if self.search_type == "일별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT08702"
        elif self.search_type == "상세보기":
            bld = "dbms/MDC/STAT/standard/MDCSTAT08703"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT08701"

        data = {
            "bld": bld,
            "inqTpCd": self.search_type,
            "inqCondTpCd1": self.trade_index,
            "inqCondTpCd2": self.trade_check,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def elw_trade_performance_per_basic_asset(self):
        """기초자산별 거래실적[13306]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT08801",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def elw_item_of_residual_expiration_status(self):
        """개별종목 잔존만기현황[13307]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT08901",
            "elwEoTpCd": self.search_type,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def elw_item_of_beneficial_expiration_status(self):
        """개별종목 만기손익현황[13308]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT09001",
            "elwEoTpCd": self.search_type,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def elw_approach_level_of_early_close(self):
        """조기종료 접근[13309]"""
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT09201", "trdDd": self.date}
        return self.update_requested_data(data)

    def elw_log_of_early_close(self):
        """조기종료 발생내역[13310]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT09301",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def elw_status_of_floating_per_basic_asset(self):
        """기초자산별 상장현황[13311]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT09401",
            "elwRghtTpKindCd": self.search_type,
            "elwUlyTpCd": self.basic_asset,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def elw_status_of_floating_per_issuing(self):
        """발행사별 상장현황[13312]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT09501",
            "elwEoTpCd": self.search_type,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def elw_assessment_of_LP_per_quarter(self):
        """분기별 LP 평가 [13313]"""
        """Web page error """
        pass
