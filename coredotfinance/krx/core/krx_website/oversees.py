# -*- coding: utf-8 -*-
from coredotfinance.krx.core.krx_website.info import Info


class Oversees(Info):
    def __init__(self, code, start, end, day, code_to_function):
        super().__init__(start, end, day)
        self.get_requested_data = code_to_function[code]


class EUREX(Oversees):
    def __init__(self, code, start, end, day, **kwargs):
        code_to_function = {
            "17101": "Requested JSON parse failed. [Failed]",
            "17102": "No data",
            "17103": "No data",
            "17104": self.trend_of_trade_perform_per_right_type,
            "17105": self.trend_of_trade_perform_per_right_type_monthly,
            "17106": self.price_table_per_expire,
            "17107": "No data",
            "17108": self.price_trend_of_EURO_STOXX,
        }
        self.right_type = kwargs.get("right_type", None)
        self.inquiry = kwargs.get("inquiry", None)
        super(EUREX, self).__init__(code, start, end, day, code_to_function)

    def trend_of_trade_perform_per_right_type(self):
        """권리유형별 거래실적 추이[17104]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT16501",
            "rghtTpCd": self.right_type,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def trend_of_trade_perform_per_right_type_monthly(self):
        """권리유형별 거래실적 추이(월)[17105]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT16601",
            "rghtTpCd": self.right_type,
            "strtYy": self.start[:4],
            "strtMm": self.start[4:6],
            "endYy": self.end[:4],
            "endMm": self.end[4:6],
        }
        return self.update_requested_data(data)

    def price_table_per_expire(self):
        """만기별 가격표(옵션)[17106]"""
        if self.inquiry == "총거래량":
            bld = "dbms/MDC/STAT/standard/MDCSTAT16802"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT16801"

        data = {"bld": bld, "trdDd": self.day[:6]}
        return self.update_requested_data(data)

    def price_trend_of_EURO_STOXX(self):
        """EURO STOXX 50 시세 추이[17108]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT16701",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)


class TokyoExchange(Oversees):
    pass  # No data
