# -*- coding: utf-8 -*-
import finance
from finance.statistics.basic.index import Index
import datetime

data = finance.data_reader('12021', search_type='개별추이', division='kospi', stk_code='207940')
print(data)