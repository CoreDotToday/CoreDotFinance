from coredotfinance.krx.core import webio


class Info:
    def __init__(self, start, end, date):
        """지수
        :param start: 시작일
        :param end: 종료일
        :param date: 기준일
        """

        self.start = start
        self.end = end
        self.day = date

    def update_requested_data(self, requested_data):
        requested_data["MIME Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        requested_data["csvxls_isNo"] = "false"
        return requested_data

    def autocomplete(self, symbol, kind):
        """
        Returns data_nm, data_cd, data_tp from below result of requests.

        Parameters
        ----------
        symbol : str
            symbol user inputs.
        kind : str
            by the type, data

        See Also
        -------
        below is the result of requests.post(url, data)
        html.content :
        b'{
            "block1": [
                {
                    "full_code": "KR7006401004",
                    "short_code": "006405",
                    "codeName": "\xec\x82\xbc\xec\x84\xb1SDI\xec\x9a\xb0",
                    "marketCode": "STK",
                    "marketName": "\xec\x9c\xa0\xea\xb0\x80\xec\xa6\x9d\xea\xb6\x8c",
                    "marketEngName": "KOSPI",
                    "ord1": "999",
                    "ord2": "16",
                }
            ],
            "CURRENT_DATETIME": "2021.06.18 PM 06:15:00",
        }'

        eval(html.content) :
            "block1": [
                {
                    "full_code": "KR7006401004",
                    "short_code": "006405",
                    "codeName": "삼성SDI우",
                    "marketCode": "STK",
                    "marketName": "유가증권",
                    "marketEngName": "KOSPI",
                    "ord1": "999",
                    "ord2": "16",
                }
            ],
            "CURRENT_DATETIME": "2021.06.18 PM 06:15:00",
        }

        Error
        -----
        When something goes wrong, html.content looks like below
        html.content:
            b'{"block1":[],"CURRENT_DATETIME":"2021.06.22 AM 10:21:54"}'
        """
        url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
        post_data = {
            "stock": {
                "mktsel": "ALL",
                "searchText": symbol,
                "bld": "dbms/comm/finder/finder_stkisu",
            },
            "product": {
                "mktsel": "ALL",
                "searchText": symbol,
                "bld": "dbms/comm/finder/finder_secuprodisu",
            },
        }
        html = webio.post(url=url, data=post_data[kind])
        html_list = eval(html.content)["block1"]
        if not html_list:
            raise ValueError(f"Can not find any data from krx. symbol : {symbol}, kind : {kind}")
        else:
            html_dict = html_list[0]
            return html_dict["codeName"], html_dict["full_code"], html_dict["short_code"]
