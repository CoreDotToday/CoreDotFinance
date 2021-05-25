# -*- coding: utf-8 -*-

from datetime import datetime
import re


def classifier(param, item_type=None):
    # 종목코드는 최소 6자리다. 6자리 이하는 종목 이름이라고 생각할 수 있다.
    if len(param) < 6:
        return "item name"

    if item_type == "elw":
        match = re.match(r"[0-9]{2}..[0-9]{2}", param)
        if match is None:
            return "item name"
        elif match[0] == param:
            return "item code"
        else:
            return "item name"

    # 주식의 종목 코드같은 경우 마지막 글자가 알파벳인 경우가 있다.
    # 그래서 param[:-1]을 해준것.
    if re.match(r"[0-9]*", param[:-1])[0] == param[:-1]:
        return "item code"
    else:
        return "item name"


def week_day(date):
    y = int(date[:4])
    m = int(date[4:6])
    d = int(date[6:])
    return datetime.weekday(datetime(y, m, d))


def start_end_validation(start, end):
    #  Make StartEndError
    if start is None and end is None:
        # 전종목
        return True
    elif end is None:
        # from start to 60 days later
        return True

    start = str(start)
    end = str(end)

    if len(start) != 8 or len(end) != 8:
        raise Exception('StartEndError("start and end have to be 8-digit")')
    elif start > end:
        raise Exception('StartEndError("start has to be earlier than end)')
    elif start < end:
        # from start to end
        return True
    elif start == end:
        weekday = week_day(start)
        if weekday == 5:
            raise Exception('StartEndError("start and end are Saturday")')
        elif weekday == 6:
            raise Exception('StartEndError("start and end are Sunday")')
        else:
            return True
    else:
        raise ValueError("start and end have to be 8-digit number ")
