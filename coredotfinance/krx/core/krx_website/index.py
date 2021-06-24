# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from coredotfinance.krx.core.krx_website.info import Info


class Index(Info):
    def __init__(self, code, code_to_function, start, end, day):
        self.get_requested_data = code_to_function[code]
        super(Index, self).__init__(start, end, day)


class StockIndex(Index):
    def __init__(self, code, start, end, day, division, item, **kwargs):
        """주가지수
        :param code: 항목 고유 번호
        :param start: 시작일
        :param end: 종료일
        :param day: 조회일자
        :param division:
        :param item:
        """
        code_to_function = {
            "11001": self.price_of_entire_index,
            "11002": self.fluc_of_entire_index,
            "11003": self.trend_of_index_price,
            "11004": self.info_of_entire_index,
            "11005": "Not now",
            "11006": self.stocks_of_index,
            "11007": self.per_pbr_dividend_of_index,
        }

        super().__init__(code, code_to_function, start, end, day)
        self.data_nm, self.data_cd, self.data_tp = self.autocomplete(item, "index")
        self.division = "KRX" if division is None else division.upper()
        self.search_type = kwargs.get("search_type", "전체지수")

    def price_of_entire_index(self):
        """전체 지수 시세 [11001]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT00101",
            "idxIndMidclssCd": self.division,
            "trdDd": self.day,
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
            "trdDd": self.day,
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
            "trdDd": self.day,
        }
        return self.update_requested_data(data)


class BondIndex(Index):
    def __init__(self, code, start, end, day, division):
        """
        :param code:
        :param start:
        :param end:
        :param day:
        :param division:
        """

        code_to_function = {
            "11008": self.price_of_entire_index,
            "11009": self.trend_of_index,
        }
        super().__init__(code, code_to_function, start, end, day)

        self.division = "KRX채권" if division is None else division.upper()

    def price_of_entire_index(self):
        """전체 지수 시세 [11008]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT00801",
            "trdDd": self.day,
        }
        return self.update_requested_data(data)

    def trend_of_index(self):
        """개별 지수 시세 추이 [11009]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT00901",
            "indTp": self.division,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)


class DerivationIndex(Index):
    def __init__(self, code, start, end, day, division, item):
        code_to_function = {
            "11010": self.price_of_entire_index,
            "11011": self.fluc_of_entire_index,
            "11012": self.trend_of_index,
            "11013": self.info_of_entire_index,
            "11014": "Not now",
        }
        super().__init__(code, code_to_function, start, end, day)
        if item:
            self.data_nm, self.data_cd, self.data_tp = self.autocomplete(item)
        self.division = "선물지수" if division is None else division.upper()
        self.update_requested_data = code_to_function[code]

    def autocomplete(self, item):
        if item is None:
            item = "코스피 200 선물지수"
        index_autocomplete_url = "http://data.krx.co.kr/comm/finder/autocomplete.jspx?contextName=finder_drvetcidx&value={value}&viewCount=5&bldPath=%2Fdbms%2Fcomm%2Ffinder%2Ffinder_drvetcidx_autocomplete"
        response = requests.get(index_autocomplete_url.format(value=item))
        soup = bs(response.content, "html.parser").li

        if soup is None:
            raise AttributeError(f"{item} is Wrong name as an index name")

        data_nm = soup.attrs["data-nm"]
        data_cd = soup.attrs["data-cd"]
        data_tp = soup.attrs["data-tp"]

        return data_nm, data_cd, data_tp

    def price_of_entire_index(self):
        """전체 지수 시세 [11010]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01001",
            "clssCd": self.division,
            "trdDd": self.day,
        }
        return self.update_requested_data(data)

    def fluc_of_entire_index(self):
        """전체 지수 등락률 [11011]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01101",
            "clssCd": self.division,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def trend_of_index(self):
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

    def info_of_entire_index(self):
        """전체 지수 기본 정보 [11013]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT01301",
            "idxTp": self.division,
        }
        return self.update_requested_data(data)
