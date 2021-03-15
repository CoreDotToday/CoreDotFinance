# -*- coding: utf-8 -*-
import finance
from finance.statistics.basic.index import Index
import datetime

data = finance.data_reader('11002', day=20210121, division='kospi')

print(data)