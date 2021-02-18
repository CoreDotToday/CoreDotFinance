import json
from datetime import datetime, timedelta

import requests

class Info:
    def __init__(self, code, start, end, day):
        """ 지수
        :param code: 항목 고유 번호
        :param start: 시작일
        :param end: 종료일
        :param day: 기준일
        """
        today = datetime.now()
        a_month_ago = today - timedelta(days=60)
        self.code = code
        self.start = a_month_ago.strftime('%Y%m%d') if start is None else str(start)
        self.end = today.strftime('%Y%m%d') if end is None else str(end)
        self.day = today.strftime('%Y%m%d') if day is None else str(day)

        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'
        }
        self.url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    def requests_data(self, data, new_col_map=None):
        data['MIME Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        data['csvxls_isNo'] = 'false'
        r = requests.post(self.url, data=data, headers=self.headers)
        data = json.loads(r.content)
        return data

    def read(self):
        return self.function()
