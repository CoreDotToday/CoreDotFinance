from coredotfinance.data import KrxReader

krx = KrxReader()

"""
test는 참 쉽다. 그냥 뭐가 잘 동작하고 뭐가 동작을 안하는지 알려주는 거다
그러면 뭐를 테스트하면 되는지를 알아보며ㅑㄴ 된다. 
1. 무적권 결과가 나오는 것을 물어보자
    1. 삼송빵집의 종가
    -> krx.read('005930' , start='2021-04-06', end='2021-04-06')
    이러케 해서 종가를 기준으로 물어보자.!
    과거 데이터가 갑자기 변할 일을 없지 않갔어?

    2. 카카오의 수정주과
    -> krx.read('035720', start='2021-04-09', end='2021-04-15')
    이로케 해서 09일의 가격이 수정된 것인가를 확인하는 것이디~!
    과거 데이터가 값자기 변할일이 있갔어?
    
    3. read_date 도 확인해 보지 않갔어?
    -> krx.read_data('2021-04-09')
    이로케 해서 어떤 주식의 주가를 한번 보고 그것으로다가 확인은 하는것이제
    과거 제이터가 갑자기 변하겄어?
"""


# read check
def test_krx_read():
    dataframe = krx.read(symbol='000660', start='2021-07-20', end='2021-07-20')
    assert dataframe['close'][0] == 118500


# read_date check
def test_krx_read_date():
    dataframe = krx.read_date(date='2021-07-20')
    assert dataframe['close'][0] == 3075


# adjust check
def test_krx_stock_adjust():
    dataframe = krx.read('035720', start='2021-04-14', end='2021-04-15', adjust=True)
    assert dataframe.loc['2021-04-14']['close'][0] == 111600


# multi index check
def test_krx_etf_read():
    dataframe = krx.read('152100', kind='etf', start='2021-04-15', end='2021-04-16')
    assert dataframe.loc['2021-04-15']['close'][0] == 44275


# multi index adjust check
def test_krx_etf_adjust():
    dataframe = krx.read('152100', kind='etf', start='2021-04-15', end='2021-04-16', adjust=True)
    assert dataframe.loc['2021-04-15']['close'][0] == 45566


# division parameter check
def test_krx_other_index():
    dataframe = krx.read('에너지', kind='other_index', start='2021-04-15', end='2021-04-16', division='선물지수')
    assert dataframe.loc['2021-04-15']['close'][0] == 1890.33

