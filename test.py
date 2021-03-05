# -*- coding: utf-8 -*-
import finance
from finance.statistics.basic.index import Index
import datetime

data = finance.data_reader('14005', market='전체', inquiry='채권유형별')
print(data)