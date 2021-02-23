import finance
from finance.statistics.basic.index import Index

data = finance.data_reader('13110', inquiry='개별종목', product='arirang 단', start=20210119, end=20210219)


print(data)