from coredotfinance.data import KrxReader, BinanceReader

krx = KrxReader()
binance = BinanceReader()


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
