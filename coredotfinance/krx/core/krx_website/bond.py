# -*- coding: utf-8 -*-
from coredotfinance.krx.core.krx_website.info import Info


class Bond(Info):
    def __init__(self, code, start, end, day, item, code_to_function):
        super(Bond, self).__init__(start, end, day)
        self.get_requested_data = code_to_function[code]
        if code in ["14011", "14021", "14023"]:
            self.data_nm, self.data_cd, self.data_tp = self.autocomplete(
                item, "publish"
            )
        else:
            self.data_nm, self.data_cd, self.data_tp = self.autocomplete(item, "bond")


class ItemPrice(Bond):
    def __init__(self, code, start, end, day, item, **kwargs):
        code_to_function = {
            "14001": self.price_of_entire_item,
            "14002": self.price_trend_of_item,
        }
        super().__init__(code, start, end, day, item, code_to_function)
        self.market = kwargs.get("market", None)

    def price_of_entire_item(self):
        """전종목 시세 [14001]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT09801",
            "mktId": self.market,
            "trdDd": self.day,
        }
        return self.update_requested_data(data)

    def price_trend_of_item(self):
        """개별종목 시세 추이 [14002]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT09901",
            "mktId": self.market,
            "isuCd": self.data_cd,
            "tboxisuCdBox0_finder_bondisu0_2": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)


class ItemInfo(Bond):
    def __init__(self, code, start, end, day, item, **kwargs):

        code_to_function = {"14003": self.info_of_entire_item, "14004": ""}
        self.bond_type = kwargs.get("bond_type", None)
        super(ItemInfo, self).__init__(code, start, end, day, item, code_to_function)

    def info_of_entire_item(self):
        """전종목 기본정보 [14003]"""
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT10001", "bndTpCd": self.bond_type}
        return self.update_requested_data(data)

    def entire_info_of_itme(self):
        """'개별종목 종합정보 [14004]"""
        """not now"""


class TradePerform(Bond):
    def __init__(self, code, start, end, day, item, **kwargs):
        code_to_function = {
            "14005": self.trade_performance_per_category,
            "14006": self.trade_performance_per_investor,
            "14007": self.trade_performance_of_bond_index_item,
            "14008": self.trade_performance_of_Repo,
        }
        super(TradePerform, self).__init__(
            code, start, end, day, item, code_to_function
        )
        self.market = kwargs.get("market", None)
        self.inquiry = kwargs.get("inquiry", None)

    def trade_performance_per_category(self):
        """종류별 거래실적 [14005]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT10201",
            "bndMktTpCd": self.market,
            "inqTpCd": self.inquiry,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def trade_performance_per_investor(self):
        """투자자별 거래실적 [14006]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT10301",
            "bndMktTpCd": self.market,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def trade_performance_of_bond_index_item(self):
        """국채지표종목 거래실적 [14007]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT10401",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def trade_performance_of_Repo(self):
        """Repo 거래실적 [14008]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT10501",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)


class Detail(Bond):
    def __init__(self, code, start, end, day, item, **kwargs):
        code_to_funciton = {
            "14009": self.price_assessment_trend_of_item,
            "14010": self.reported_price_trend_of_small_bond,
            "14011": self.search_of_public_bond,
            "14012": self.issue_info_of_public_bond,
            "14013": self.histoty_per_type_of_publication,
            "14014": self.history_of_publication_price_adjustment,
            "14015": self.prepayment,
            "14016": self.delisting_bond,
            "14017": self.rate_of_profit_of_bond_over_the_counter,
            "14018": self.rate_of_profit_of_index,
            "14019": self.strip_short_interest,
            "14020": self.substitution_price_of_bond,
            "14021": self.substitution_price_of_bond_per_issuer,
            "14022": self.substitution_price_of_bond_per_type,
            "14023": self.credit_per_issuer,
            "14024": self.publication_situation_per_credit,
            "14025": self.investment_index_of_convertible_bond,
            "14026": self.exercise_of_right_of_bond_about_stock,
            "14027": self.strike_price_of_bond_about_stock,
        }
        super().__init__(code, start, end, day, item, code_to_funciton)
        self.market = kwargs.get("market", None)
        self.inquiry = kwargs.get("inquiry", None)
        self.bond_type = kwargs.get("bond_type", None)
        self.search_type = kwargs.get("search_type", None)

    def price_assessment_trend_of_item(self):
        """개별종목 시가평가 추이 [14009]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT10601",
            "tboxisuCd_finder_bondisu0_0": f"{self.data_cd}/{self.data_nm}",
            "isuCd": self.data_cd,
            "codeNmisuCd_finder_bondisu0_0": self.data_nm,
            "param1isuCd_finder_bondisu0_0": 2,
            "basddTpCd": self.inquiry,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def reported_price_trend_of_small_bond(self):
        """소액채권 신고가격 추이 [14010]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT10701",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def search_of_public_bond(self):
        """상장채권 상세검색 [14011]"""
        # 기능중 채권분류 및 상세검색은 추가하지 않았음
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT10801",
            "tboxisurCd_finder_bndordisu0_2": f"{self.data_tp}/{self.data_nm}",
            "isurCd": self.data_tp,
            "isurCd2": self.data_tp,
            "codeNmisurCd_finder_bndordisu0_2": self.data_nm,
            "bndTpCd": self.bond_type,
        }
        return self.update_requested_data(data)

    def issue_info_of_public_bond(self):
        """상장채권 발행정보 [14012]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT10901",
            "tboxisuCd_finder_bondisu0_2": f"{self.data_cd}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_cd,
            "codeNmisuCd_finder_bondisu0_2": self.data_nm,
        }
        return self.update_requested_data(data)

    def histoty_per_type_of_publication(self):
        """상장유형별 내역 [14013]"""
        if self.search_type == "추가":
            bld = "dbms/MDC/STAT/standard/MDCSTAT11002"
        elif self.search_type == "변경":
            bld = "dbms/MDC/STAT/standard/MDCSTAT11003"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT11001"

        data = {
            "bld": bld,
            "inqTpCd": self.search_type,
            "BndMktactTpCd": self.bond_type,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def history_of_publication_price_adjustment(self):
        """상장금액조정 내역 [14014]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT11101",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def prepayment(self):
        """중도상환 [14015]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT11201",
            "bndMktactTpCd": self.inquiry,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def delisting_bond(self):
        """채권상장폐지 [14016]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT11301",
            "bndDelistRsnCd": self.inquiry,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def rate_of_profit_of_bond_over_the_counter(self):
        """장외 채권수익률 [14017]"""
        #### ExecuteForResourceBundle 의 url이 requests.get으로 안받아와진다!!
        #### http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?baseName=krx.mdc.i18n.component&key=B160.bld&type=kospi
        if self.search_type == "개별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT11402"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT11401"
        output = {
            "국고채 1년": "3006",
            "국고채 2년": "3019",
            "국고채 3년": "3000",
            "국고채 5년": "3007",
            "국고채 10년": "3013",
            "국고채 20년": "3014",
            "국고채 30년": "3017",
            "국민주택 1종 5년": "3008",
            "회사채 AA-(무보증 3년)": "3009",
            "회사채 BBB- (무보증 3년)": "3010",
            "CD(91일)": "4000",
        }
        data = {
            "bld": bld,
            "inqTpCd": self.search_type,
            "trdDd": self.day,
            "bndKindTpCd": output[self.bond_type],
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def rate_of_profit_of_index(self):
        """지표 수익률 [14018]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT11501",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def strip_short_interest(self):
        """스트립 단기금리 [14019]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT11601",
            "inqTpCd": self.inquiry,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def substitution_price_of_bond(self):
        """채권 대용가 [14020]"""
        if self.search_type == "개별추이":
            bld = None  # jsGrid_dict를 찾지 못함...
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT11701"
        data = {
            "bld": bld,
            "tboxisuCd_finder_bondisu0_10": f"{self.data_cd}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_cd,
            "codeNmisuCd_finder_bondisu0_10": self.data_nm,
            "param1isuCd_finder_bondisu0_10": 2,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def substitution_price_of_bond_per_issuer(self):
        """발행기관별 채권 대용가 [14021]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT11801",
            "tboxisurCd_finder_bndordisu0_1": f"{self.data_tp}/{self.data_nm}",
            "isurCd": self.data_tp,
            "isurCd2": self.data_tp,
            "codeNmisurCd_finder_bndordisu0_1": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def substitution_price_of_bond_per_type(self):
        """유형별 채권 대용가 [14022]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT11901",
            "bndTpCd": self.bond_type,
            "bndClssCd": self.inquiry,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def credit_per_issuer(self):
        """발행기관별 신용등급 [14023]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT12001",
            "tboxisurCd_finder_bndordisu0_14": f"{self.data_tp}/{self.data_nm}",
            "isurCd": self.data_tp,
            "isurCd2": self.data_tp,
            "codeNmisurCd_finder_bndordisu0_14": self.data_nm,
            "creditValuInstCd": self.inquiry,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def publication_situation_per_credit(self):
        """신용등급별 상장현황 [14024]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT12101",
            "creditValuInstCd": self.inquiry,
            "trdDd": self.day,
        }
        return self.update_requested_data(data)

    def investment_index_of_convertible_bond(self):
        """전환사채 투자지표 [14025]"""
        data = {"bld": "dbms/MDC/STAT/standard/MDCSTAT12201", "trdDd": self.day}
        return self.update_requested_data(data)

    def exercise_of_right_of_bond_about_stock(self):
        """주식관련채권 권리행사 [14026]"""
        # 'bld': 'dbms/MDC/STAT/standard/MDCSTAT12301' 을 데이터로 사용하면 전체 데이터가 출력된다.
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT12302",
            "tboxisuCd_finder_bondisu0_17": f"{self.data_cd}/{self.data_nm}",
            "isuCd": self.data_cd,
            "isuCd2": self.data_cd,
            "param1isuCd_finder_bondisu0_17": 2,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def strike_price_of_bond_about_stock(self):
        """주식관련채권 행사가액 [14027]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT12401",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)
