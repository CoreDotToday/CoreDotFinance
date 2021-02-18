import finance
from finance.statistics.basic.index import Index

# PER/PBR/배당수익률(개별종목) [12021]
#   전종목 검색
# data = finance.data_reader('12021', division='kospi', search_type='전종목', day=20210101)
#   개별추이/종목명 검색
# data = finance.data_reader('12021', division='kospi', search_type = '개별추이', start=20210101, end=20210201, stc_name='삼성전자')
#   개별추이/종목코드 검색
data = finance.data_reader('12021', division='kospi', search_type = '개별추이', start=20210101, end=20210201, stc_code='005930')

print(data)


