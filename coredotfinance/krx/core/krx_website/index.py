# -*- coding: utf-8 -*-
from coredotfinance.krx.core.krx_website.info import Info


class Index(Info):
    def __init__(self, code,  start, end, date, **kwargs):
        code_to_function = {
            "11001": self.price_of_entire_index,
            "11002": self.fluc_of_entire_index,
            "11003": self.trend_of_index_price,
            "11004": self.info_of_entire_index,
            "11005": "Not now",
            "11006": self.stocks_of_index,
            "11007": self.per_pbr_dividend_of_index,
            "11008": self.bond_price_of_entire_index,
            "11009": self.bond_trend_of_index,
            "11010": self.derivative_price_of_entire_index,
            "11011": self.derivative_fluc_of_entire_index,
            "11012": self.derivative_trend_of_index,
            "11013": self.derivative_info_of_entire_index,
            "11014": "Not now",
        }
        super(Index, self).__init__(start, end, date)
        self.division = kwargs.get('division', 'KRX').upper()
        symbol = kwargs.get('symbol')
        if symbol:
            if self.division in ['KRX', 'KOSPI', 'KOSDAQ', '테마']:
                self.data_nm, self.data_cd, self.data_tp = self.autocomplete(
                    symbol=symbol,
                    kind='index'
                )
            else:
                self.data_nm, self.data_cd, self.data_tp = self.autocomplete(
                    symbol=symbol,
                    kind='other_index',
                    division=self.division
                )
        self.search_type = kwargs.get("search_type", "전체지수")
        self.get_requested_data = code_to_function[code]

    def price_of_entire_index(self):
        """전체 지수 시세 [11001]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT00101",
            "idxIndMidclssCd": self.division,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def fluc_of_entire_index(self):
        """전체 지수 변동률 [11002]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT00201",
            "idxIndMidclssCd": self.division,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def trend_of_index_price(self):
        """개별 지수 시세추이 [11003]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT00301",
            "tboxindIdx_finder_equidx0_0": self.data_nm,
            "indIdx": self.data_cd,
            "indIdx2": self.data_tp,
            "codeNmindIdx_finder_equidx0_0": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def info_of_entire_index(self):
        """전체 지수 기본 정보 [11004]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT00401",
            "idxIndMidclssCd": self.division,
        }
        return self.update_requested_data(data)

    def info_of_index(self):
        """개별 지수 종합 정보 [11005]"""
        pass

    def stocks_of_index(self):
        """지구 구성 종목 [11006]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT00601",
            "tboxindIdx_finder_equidx0_2": self.data_nm,
            "indIdx": self.data_cd,
            "indIdx2": self.data_tp,
            "codeNmindIdx_finder_equidx0_2": self.data_nm,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def per_pbr_dividend_of_index(self):
        """개별지수 PER/PBR/배당수익률 [11007]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT00702",
            "searchType": self.search_type,
            "indTpCd": self.data_cd,
            "indTpCd2": self.data_tp,
            "codeNmindTpCd_finder_equidx0_3": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
            "idxIndMidclssCd": self.division,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def bond_price_of_entire_index(self):
        """전체 지수 시세 [11008]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT00801",
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def bond_trend_of_index(self):
        """개별 지수 시세 추이 [11009]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT00901",
            "indTp": self.division,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def derivative_price_of_entire_index(self):
        """전체 지수 시세 [11010]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01001",
            "clssCd": self.division,
            "trdDd": self.date,
        }
        return self.update_requested_data(data)

    def derivative_fluc_of_entire_index(self):
        """전체 지수 등락률 [11011]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01101",
            "clssCd": self.division,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def derivative_trend_of_index(self):
        """개별 지수 시세 추이 [11012]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01201",
            "indTpCd": self.data_cd,
            "idxIndCd": self.data_tp,
            "tboxidxCd_finder_drvetcidx0_0": self.data_nm,
            "idxCd": self.data_cd,
            "idxCd2": self.data_tp,
            "codeNmidxCd_finder_drvetcidx0_0": self.data_nm,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def derivative_info_of_entire_index(self):
        """전체 지수 기본 정보 [11013]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01301",
            "idxTp": self.division,
        }
        return self.update_requested_data(data)

