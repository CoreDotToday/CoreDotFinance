import finance
from finance.statistics.basic.index import Index

data = finance.data_reader('12021', division='kospi', search_type = '개별추이', start=20210101, end=20210201, stk_name='기아')

print(data)


