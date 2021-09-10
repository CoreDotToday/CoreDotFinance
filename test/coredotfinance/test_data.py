import pytest
from datetime import datetime, timedelta

from coredotfinance.data import BinanceReader, KrxReader


binance = BinanceReader()
krx = KrxReader()

# ---------------------------- krx -----------------------------------
# ---------------------------- krx read -----------------------------------


# read
def test_krx_read():
    dataframe = krx.read(symbol="000660", start="2021-07-20", end="2021-07-20")
    assert dataframe["close"][0] == 118500


# per
def test_krx_per_read():
    dataframe = krx.read("000660", kind="per", start="2021-04-15", end="2021-04-16")
    assert dataframe.loc["2021-04-15"]["close"][0] == 137500


# multi index
def test_krx_etf_read():
    dataframe = krx.read("152100", kind="etf", start="2021-04-15", end="2021-04-16")
    assert dataframe.loc["2021-04-15"]["close"][0] == 44275


# etn
def test_krx_etn_read():
    dataframe = krx.read("500011", start="2021-09-01", end="2021-09-02", kind="etn")
    assert dataframe.loc["2021-09-02"]["close"][0] == 10280


# elw
def test_krx_elw_read():
    dataframe = krx.read("58G194", start="2021-09-01", end="2021-09-02", kind="elw")
    assert dataframe.loc["2021-09-02"]["close"][0] == 20


# index
def test_krx_index_read():
    dataframe = krx.read("krx 100", start="2021-09-01", end="2021-09-02", kind="index")
    assert dataframe.loc["2021-09-02"]["close"][0] == 6560.56


# division parameter
def test_krx_other_index_read():
    dataframe = krx.read(
        "에너지", kind="other_index", start="2021-04-15", end="2021-04-16", division="선물지수"
    )
    assert dataframe.loc["2021-04-15"]["close"][0] == 1890.33


# ---------------------------- krx read_date -----------------------------------

# read_date
def test_krx_read_date():
    dataframe = krx.read_date(date="1996-01-09")
    assert dataframe["symbol"][0] == "009840"


def test_krx_read_date_per():
    dataframe = krx.read_date(date="1996-01-09", kind="per")
    assert dataframe["symbol"][0] == "009840"


def test_krx_read_date_etf():
    dataframe = krx.read_date(date="2010-01-09", kind="etf")
    assert dataframe["symbol"][0] == "108630"


def test_krx_read_date_etn():
    dataframe = krx.read_date(date="2015-01-09", kind="etn")
    assert dataframe["symbol"][0] == "530001"


def test_krx_read_date_elw():
    dataframe = krx.read_date(date="2015-01-09", kind="elw")
    assert dataframe["symbol"][0] == "754474"


def test_krx_read_date_index():
    dataframe = krx.read_date(date="2015-01-09", kind="index")
    assert dataframe["index_name"][0] == "KRX 100"


def test_krx_read_date_other_index():
    dataframe = krx.read_date(date="2015-01-09", kind="other_index", division="선물지수")
    assert dataframe["index_name"][0] == "미국달러선물지수"


# ---------------------------- krx read_all -----------------------------------

# read_all
def test_krx_read_all():
    dataframe = krx.read_all(symbol="323410")
    assert dataframe.loc["2021-09-02"]["close"][0] == 81900


# ---------------------------- krx functions & options -------------------------------

# krx_search
def test_krx_search():
    search_tuple = krx.search("삼성전자")
    assert search_tuple == ("삼성전자", "KR7005930003", "005930")


# listed_company
def test_krx_listed_company():
    dataframe = krx.listed_company()
    is_skhynix = dataframe["종목코드"] == "000660"
    skhynixdata = dataframe[is_skhynix]
    assert skhynixdata["종목명"].to_list()[0] == "SK하이닉스"


# multi index adjust
def test_krx_etf_adjust():
    dataframe = krx.read(
        "152100", kind="etf", start="2021-04-15", end="2021-04-16", adjust=True
    )
    assert dataframe.loc["2021-04-15"]["close"][0] == 45566


# adjust, kor
def test_krx_stock_with_options():
    dataframe = krx.read(
        "035720", start="2021-04-14", end="2021-04-15", adjust=True, kor=True
    )
    assert dataframe.loc["2021-04-14"]["종가"][0] == 111600


# ---------------------------- krx Error -----------------------------------

# Wrong symbol to get data
def test_krx_wrong_symbol():
    with pytest.raises(ValueError):
        krx.read(symbol="0006600", start="2021-07-01", end="2021-07-10")


# No data Exception
def test_krx_no_data():
    with pytest.raises(Exception):
        krx.read(symbol="000660", start="3021-07-01", end="3021-07-10")


# start,end is None
def test_krx_date_None():
    # start, end 모두 None 값일때 오류가 발생했다.
    # test code를 실행시킨 시점에 주식시장이 열리지 않았으면
    # Warning 이전에 Exception("No data") 가 발생한다.
    # 따라서 불러오는 데이터에 start 값은 입력하고 end 값만 None으로 준다.
    # 데이터는 통신 속도를 높이기 위해 1주일 치만 불러온다.

    start = str(datetime.today().date() - timedelta(7))
    with pytest.warns(UserWarning):
        krx.read(symbol="000660", start=start)


# start > end
def test_krx_date_wrong():
    with pytest.raises(ValueError):
        krx.read(symbol="000660", start="2021-07-20", end="2021-07-10")
    with pytest.raises(ValueError):
        krx.read(symbol="000660", start="20210720", end="20210730")


# not expected_kind
def test_krx_not_expected_kind():
    with pytest.raises(ValueError):
        krx.read(
            symbol="000660",
            kind="Not expected_list",
            start="2021-07-20",
            end="2021-07-20",
        )


# when start, end is None
def test_krx_read_date_None():
    # test_krx_date_None 의 경우와는 다르게
    # read_date는 Exception("No data") 를 발생시키지 않는다.

    with pytest.warns(UserWarning):
        krx.read_date()


# when try to get adjust data from read_date
def test_krx_read_date_adjust():
    with pytest.warns(UserWarning):
        krx.read_date("1996-01-09", adjust=True)


# ---------------------------- binance -----------------------------------


def test_binance_read():
    dataframe = binance.read(
        "ETHBTC", start="2021-03-01", end="2021-03-21", interval="1m"
    )
    assert dataframe.loc["2021-03-01 16:39:00"]["close"][0] == 0.031474


def test_binance_symbol_list():
    symbol_list = binance.symbol_list()
    assert isinstance(symbol_list, list)
    assert len(symbol_list) > 100
    assert "ETHBTC" in symbol_list  # ETHBTC 가 symbol_list에 없으면 이상이 있다고 판단하자


def test_binance_interval_list():
    interval_list = binance.interval_list()
    assert interval_list == [
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "4h",
        "6h",
        "8h",
        "12h",
        "1d",
        "3d",
        "1w",
        "1M",
    ]
