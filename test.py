# -*- coding: utf-8 -*-
import finance
from finance.statistics.basic.index import Index
import datetime

# data = finance.data_reader('12002', start=20210310, end=20210317, division='전체')
# data = finance.data_reader('12002', start=20210310, end=20210317, division='전체', detail='수정주가 적용')
data = finance.data_reader('11003', i)
print(data)

