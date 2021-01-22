import finance as f
from finance.statistics.basic.index import Index


# d = f.data_reader(11004, ind_name='리츠인프라·우선주 혼합지수')
d = f.data_reader('11009')


print(d)
