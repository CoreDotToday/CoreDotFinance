# -*- coding: utf-8 -*-
from coredotfinance.krx.core.krx_website.info import Info


class Derivative(Info):
    def __init__(self, code, start, end, day, item, code_to_function, kwargs):
        super().__init__(start, end, day)
        self.get_requested_data = code_to_function[code]
        if code in ["15002"]:
            self.data_nm, self.data_cd, self.data_tp = self.autocomplete(
                item, "derivative"
            )
        self.item = item
        self.inquiry = kwargs.get("inquiry", None)
        self.trade_index = kwargs.get("trade_index", None)
        self.trade_check = kwargs.get("trade_check", None)
        self.market = kwargs.get("market", None)
        self.right_type = kwargs.get("right_type", None)
        self.detail = kwargs.get("detail", None)
        self.search_type = kwargs.get("search_type", None)


class ItemPrice(Derivative):
    def __init__(self, code, start, end, day, item, **kwargs):
        code_to_function = {
            "15001": self.price_of_entire_item,
            "15002": self.price_trend_of_item,
            "15003": self.price_trend_of_futures,
        }
        super().__init__(code, start, end, day, item, code_to_function, kwargs)

    def price_of_entire_item(self):
        """전종목 시세[15001]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT12501",
            "trdDd": self.day,
            "prodId": self.item,
            "mktTpCd": self.market,
        }
        return self.update_requested_data(data)

    def price_trend_of_item(self):
        """개별시세 추이[15002]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT12601",
            "strtDd": self.start,
            "endDd": self.end,
            "tboxisuCd_finder_drvprodisu0_1": f"{self.data_tp}/ {self.data_nm}",
            "isuCd": self.data_cd,
        }
        return self.update_requested_data(data)

    def price_trend_of_futures(self):
        """최근월물 시세 추이(선물)[15003]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT12701",
            "prodId": self.item,
            #'subProdId': self.detail, # subProdId를 불러오는데 문제가 있었
            "strtDd": self.start,
            "endDd": self.end,
            "mktTpCd": self.market,
        }
        return self.update_requested_data(data)


class ItemInfo(Derivative):
    def __init__(self, code, start, end, day, item, **kwargs):
        code_to_function = {
            "15004": self.info_of_entire_item,
            "15005": self.info_of_item,
        }
        super().__init__(code, start, end, day, item, code_to_function, kwargs)

    def info_of_entire_item(self):
        """전종목 기본정보[15004]"""
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT12801", "prodId": self.item}
        return self.update_requested_data(data)

    def info_of_item(self):
        """개별종목 종합정보[15005]"""
        return "Not now"


class TradePerform(Derivative):
    def __init__(self, code, start, end, day, item, **kwargs):
        code_to_function = {
            "15006": self.trade_perform_of_entire_item,
            "15007": self.trade_perform_ber_invastor,
            "15008": self.trend_of_consulted_big_trade_performance,
            "15009": self.trade_performance_of_basic_asset,
        }
        super().__init__(code, start, end, day, item, code_to_function, kwargs)

    def trade_perform_of_entire_item(self):
        """전체상품 거래실적[15006]"""
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT13001", "trdDd": self.day}
        return self.update_requested_data(data)

    def trade_perform_ber_invastor(self):
        """투자자별 거래실적[15007]"""
        if self.search_type == "개별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT13102"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT13101"
        data = {
            "bld": bld,
            "isuCd": self.item,
            "strtDd": self.start,
            "endDd": self.end,
            "inqTpCd": self.search_type,
            "prtType": self.trade_index,
            "prtCheck": self.trade_check,
            "juya": self.market,
        }
        return self.update_requested_data(data)

    def trend_of_consulted_big_trade_performance(self):
        """협의대향거래실적 추이[15008]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT13201",
            "isuCd": self.item,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def trade_performance_of_basic_asset(self):
        """기초자산별 거래실적(주식/선물/옵션)[15009]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT13301",
            "secugrpId": self.item,
            "isuOpt": self.right_type,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)


class Detail(Derivative):
    def __init__(self, code, start, end, day, item, **kwargs):
        code_to_function = {
            "15010": self.future_trend_of_basis,
            "15011": self.trend_of_implied_volatility,
            "15012": self.trend_of_pc_ratio,
            "15013": self.price_table_per_expiration_and_discount,
            "15014": self.trend_of_pork_price,
            "15015": self.sudden_change_of_setting_price,
            "15016": self.ratio_of_low_exercise_of_right,
        }
        super().__init__(code, start, end, day, item, code_to_function, kwargs)

    def future_trend_of_basis(self):
        """베이시스 추이(선물)[15010]"""
        if self.search_type == "개별종목":
            bld = "dbms/MDC/STAT/standard/MDCSTAT13402"
            data_cd, data_nm, data_tp = self.autocomplete(self.item, "derivative")
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT13401"
            data_cd, data_nm, data_tp = None, None, None
        data = {
            "bld": bld,
            "secugrpId": self.search_type,
            "prodId": self.item,
            "expmmNo": self.detail,
            "tboxisuCd_finder_drvfuprodisu1_1": f"{data_tp}/{data_nm}",
            "isuCd": data_cd,
            "isuCd2": self.item,
            "codeNmisuCd_finder_drvfuprodisu1_1": data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def trend_of_implied_volatility(self):
        """내재변동성 추이(옵션)[15011]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT13501",
            "prodId": self.item,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def trend_of_pc_ratio(self):
        """P/C Ratio 추이(옵션)[15012]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT13601",
            "prodId": self.item,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def price_table_per_expiration_and_discount(self):
        """행사가격/만기별 가격표(옵션)[15013]"""
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT13701", "prodId": self.item}
        return "Not now"  # 표를 띄우는 것이 쉽지 않음..

    def trend_of_pork_price(self):
        """돈육시세 동향[15014]"""
        if self.inquiry == "현재가":
            bld = "dbms/MDC/STAT/standard/MDCSTAT13801"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT13802"
        data = {"bld": bld, "strtDd": self.start, "endDd": self.end}
        return self.update_requested_data(data)

    def sudden_change_of_setting_price(self):
        """최종결제가격 급변[15015] (기간별조회)"""
        year = self.day[:4]
        month = self.day[4:6]
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT14001",
            "trdYy": year,
            "trdMm": month,
            "cpType": self.inquiry,
        }
        #  최종결제가격 급변은 표를 띄우는 것이 쉽지 않음..
        #  데이터가 jsp 파일 안에 있음
        return self.update_requested_data(data)

    def ratio_of_low_exercise_of_right(self):
        """낮은 권리행사 배율[15016] (기간별조회)"""
        str_year = self.start[:4]
        str_month = self.start[4:6]
        end_year = self.end[:4]
        end_month = self.end[4:6]
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT14101",
            "strtYy": str_year,
            "strtMm": str_month,
            "endYy": end_year,
            "endMm": end_month,
        }
        #  최종결제가격 급변은 표를 띄우는 것이 쉽지 않음..
        #  데이터가 jsp 파일 안에 있음
        #  데이터 단위가 %인데 표시되어 있지 않음
        return self.update_requested_data(data)
