import pytest

from coredotfinance.data import BinanceReader, KrxReader


binance = BinanceReader()
krx = KrxReader()


def test_binance_read():
    dataframe = binance.read(
        "ETHBTC", start="2021-03-01", end="2021-03-21", interval="1m"
    )
    assert dataframe.loc["2021-03-01 16:39:00"]["close"][0] == 0.031474


# read check
def test_krx_read():
    dataframe = krx.read(symbol="000660", start="2021-07-20", end="2021-07-20")
    assert dataframe["close"][0] == 118500


# date is None check
def test_krx_date_None():
    with pytest.warns(UserWarning):
        krx.read(symbol="000660")


# start > end check
def test_krx_date_wrong():
    with pytest.raises(ValueError):
        krx.read(symbol="000660", start="2021-07-20", end="2021-07-10")
        krx.read(symbol="000660", start="20210720", end="20210730")


# listed_company
def test_krx_listed_company():
    dataframe = krx.listed_company()
    is_skhynix = dataframe["종목코드"] == "000660"
    skhynixdata = dataframe[is_skhynix]
    assert skhynixdata["종목명"].to_list()[0] == "SK하이닉스"


# not expected_kind
def test_krx_not_expected_kind():
    with pytest.raises(ValueError):
        krx.read(
            symbol="000660",
            kind="Not expected_list",
            start="2021-07-20",
            end="2021-07-20",
        )


# read_date check
def test_krx_read_date():
    dataframe = krx.read_date(date="2021-07-20")
    assert dataframe["close"][0] == 3075


# read_all check
def test_krx_read_all():
    dataframe = krx.read_all(symbol="323410")
    assert dataframe.loc["2021-09-02"]["close"][0] == 81900


# adjust check
def test_krx_stock_adjust():
    dataframe = krx.read("035720", start="2021-04-14", end="2021-04-15", adjust=True)
    assert dataframe.loc["2021-04-14"]["close"][0] == 111600


# multi index check
def test_krx_etf_read():
    dataframe = krx.read("152100", kind="etf", start="2021-04-15", end="2021-04-16")
    assert dataframe.loc["2021-04-15"]["close"][0] == 44275


# multi index adjust check
def test_krx_etf_adjust():
    dataframe = krx.read(
        "152100", kind="etf", start="2021-04-15", end="2021-04-16", adjust=True
    )
    assert dataframe.loc["2021-04-15"]["close"][0] == 45566


# etn check
def test_krx_etn_read():
    dataframe = krx.read("500011", start="2021-09-01", end="2021-09-02", kind="etn")
    assert dataframe.loc["2021-09-02"]["close"][0] == 10280


# elw check
def test_krx_elw_read():
    dataframe = krx.read("58G187", start="2021-09-01", end="2021-09-02", kind="elw")
    assert dataframe.loc["2021-09-02"]["close"][0] == 10


# index check
def test_krx_index_read():
    dataframe = krx.read("krx 100", start="2021-09-01", end="2021-09-02", kind="index")
    assert dataframe.loc["2021-09-02"]["close"][0] == 6560.56


# division parameter check
def test_krx_other_index():
    dataframe = krx.read(
        "에너지", kind="other_index", start="2021-04-15", end="2021-04-16", division="선물지수"
    )
    assert dataframe.loc["2021-04-15"]["close"][0] == 1890.33


# per check
def test_krx_per_read():
    dataframe = krx.read("000660", kind="per", start="2021-04-15", end="2021-04-16")
    assert dataframe.loc["2021-04-15"]["close"][0] == 137500


# krx_search check
def test_krx_search():
    search_tuple = krx.search("삼성전자")
    assert search_tuple == ("삼성전자", "KR7005930003", "005930")


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
