# -*- coding: utf-8 -*-
from coredotfinance.krx.core.krx_website.info import Info


class Commodity(Info):  # 일반상품: 석유, 금, 배출
    def __init__(self, code, start, end, day, code_to_function, kwargs):
        super(Commodity, self).__init__(start, end, day)
        self.get_requested_data = code_to_function[code]
        self.trade_index = kwargs.get("trade_index", None)
        self.trade_check = kwargs.get("trade_check", None)
        self.inquiry = kwargs.get("inquiry", None)


class Oil(Commodity):  # 석유 [16101~16105]
    def __init__(self, code, start, end, day, **kwargs):
        code_to_function = {
            "16101": self.info_of_entire_items,
            "16102": self.price_trend_of_item,
            "16103": self.trade_performance_per_investor,
            "16104": self.price_domestic_gasstation,
            "16105": self.price_international,
        }
        super().__init__(code, start, end, day, code_to_function, kwargs)
        self.oil = kwargs.get("oil", None)

    def info_of_entire_items(self):
        """전종목 기본정보[16101]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT14301",
            "secugrpId": self.oil,  # ALL(전체), GA(휘발유), DI(경유), KE(등유)
        }
        return self.update_requested_data(data)

    def price_trend_of_item(self):
        """유종별 시세 추이[16102]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT14401",
            "secugrpId": self.oil,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def trade_performance_per_investor(self):
        """참가자별 거래실적[16103]"""
        if self.inquiry == "일별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT14502"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT14501"
        data = {
            "bld": bld,
            "inqTpCd": self.inquiry,  # 1(기간합계), 2(일별추이)
            "trdVolVal": self.trade_index,  # 1(거래량), 2(거래대금)
            "bidAskNet": self.trade_check,  # 1(매도), 2(매수), 3(순매수)
            "secugrpId": self.oil,  # GA(휘발유), DI(경유), KE(등유)
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def price_domestic_gasstation(self):
        """국내유가(주유소) 동향 [16104]"""
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT14601",
            "secugrpId": self.oil,  # GA(휘발유), DI(경유), KE(등유)
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def price_international(self):  # [16105] 국제유가 동향
        pass


class Gold(Commodity):  # 금 [16201~16207]
    def __init__(self, code, start, end, day, **kwargs):
        code_to_function = {
            "16201": self.price_of_entire_items,
            "16202": self.price_trend_of_item,
            "16203": self.info_of_entire_items,
            "16204": self.info_of_item,
            "16205": self.trade_performance_per_investor,
            "16206": self.block_trade,
            "16207": self.price_international,
        }

        super(Gold, self).__init__(code, start, end, day, code_to_function, kwargs)
        self.gold = kwargs.get("gold", None)

    def price_of_entire_items(self):  # [16201] 전종목 시세
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT14901",
            "trdDd": self.day,
        }
        return self.update_requested_data(data)

    def price_trend_of_item(self):  # [16202] 개별종목 시세 추이
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT15001",
            "isuCd": self.gold,
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def info_of_entire_items(self):  # [16203] 전종목 기본정보
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT15101",
        }
        return self.update_requested_data(data)

    def info_of_item(self):  # [16204] 개별종목 종합정보
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT15201",
            "isuCd": self.gold,  # KRD040200002(금 99.99K), KRD040201000(미니금 100g)
        }
        """ 데이터 총 3개
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT15202',
            'isuCd': self.gold,  # KRD040200002(금 99.99K), KRD040201000(미니금 100g)
        }
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT15203',
            'isuCd': self.gold,  # KRD040200002(금 99.99K), KRD040201000(미니금 100g)
        }
        """
        return "Not now"

    def trade_performance_per_investor(self):  # [16205] 투자자별 거래실적
        if self.inquiry == "일별추이":
            bld = "dbms/MDC/STAT/standard/MDCSTAT15302"
        else:
            bld = "dbms/MDC/STAT/standard/MDCSTAT15301"
        data = {
            "bld": bld,
            "strtDd": self.start,
            "endDd": self.end,
            "trdVolVal": self.trade_index,  # 1(거래량), 2(거래대금)
            "bidAskNet": self.trade_check,  # 1(매도), 2(매수), 3(순매수)
        }
        return self.update_requested_data(data)

    def block_trade(self):  # [16206] 협의대량거래실적 추이
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT15401",
            "strtDd": self.start,
            "endDd": self.end,
        }
        return self.update_requested_data(data)

    def price_international(self):  # [16207] 국제금시세 동향
        if self.inquiry == "현재가":
            data = {
                "bld": "dbms/MDC/STAT/standard/MDCSTAT13901",
                "strtDd": self.start,
                "endDd": self.end,
            }
        else:
            data = {
                "bld": "dbms/MDC/STAT/standard/MDCSTAT13902",
                "strtDd": self.start,
                "endDd": self.end,
            }
        return self.update_requested_data(data)


class CarbonEmission(Commodity):  # 배출권 [16301~16304]
    def __init__(self, code, start, end, day, **kwargs):
        code_to_function = {
            "16301": self.price_of_entire_items,
            "16302": self.price_trend_of_item,
            "16303": self.info_of_entire_items,
            "16304": self.info_of_item,
        }

        super(CarbonEmission, self).__init__(
            code, start, end, day, code_to_function, kwargs
        )
        self.kwargs = kwargs
        self.item = self.kwargs.get(
            "item", None
        )  # isuCd: 개별종목명 [예: KRD050022007(KAU20), KRD050032105(KAU21)]

    def price_of_entire_items(self):  # [16301] 전종목 시세
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT15601",
            "trdDd": self.day,
            #  'share': 1,  # 1~3(톤 / 천톤 / 백만톤)
            #  'money': 1,  # 1~4(원 / 천원 / 백만원 / 십억원)
        }
        return self.update_requested_data(data)

    def price_trend_of_item(self):  # [16302] 개별종목 시세 추이
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT15701",
            "isuCd": self.item,  # KRD050022007(KAU20)
            "strtDd": self.start,
            "endDd": self.end,
            #  'share': 1,  # 1~3(톤 / 천톤 / 백만톤)
            #  'money': 1,  # 1~4(원 / 천원 / 백만원 / 십억원)
        }
        return self.update_requested_data(data)

    def info_of_entire_items(self):  # [16303] 전종목 기본정보
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT15801",
        }
        return self.update_requested_data(data)

    def info_of_item(self):  # [16304] 개별종목 종합정보
        data = {
            "bld": "dbms/MDC/STAT/standard/MDCSTAT15901",
            "isuCd": self.item,  # KRD050022007(KAU20), KRD050032105(KAU21)
        }
        """ 데이터 총 3개
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT15902',
            'isuCd': self.isucd, # KRD050022007(KAU20), KRD050032105(KAU21)
        }
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT15903',
            'isuCd': self.isucd, # KRD050022007(KAU20), KRD050032105(KAU21)
        }
        """
        return "Not now"
