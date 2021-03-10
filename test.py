# -*- coding: utf-8 -*-
import finance
from finance.statistics.basic.index import Index
import datetime

data = finance.data_reader('14020', inquiry='개별추이', product='금호')

print(data)