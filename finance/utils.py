# -*- coding: utf-8 -*-

import re


def classifier(param, item_type=None):
    # 종목코드는 최소 6자리다. 6자리 이하는 종목 이름이라고 생각할 수 있다.
    if len(param) < 6:
        return 'item name'

    if item_type == 'elw':
        if re.match(r'[0-9]{2}..[0-9]{2}', param)[0] == param:
            return 'item code'
        else:
            return 'item name'

    # 주식의 종목 코드같은 경우 마지막 글자가 알파벳인 경우가 있다.
    # 그래서 param[:-1]을 해준것. 같으면 종목 코드이고 아니면 종목명이다.
    if re.match(r'[0-9]*', param[:-1])[0] == param[:-1]:
        return 'item code'
    else:
        return 'item name'

