# -*- coding: utf-8 -*-
import finance

data = finance.data_reader('13302', start=20210401, end=20210406, item_code='52F901')

print(data)



