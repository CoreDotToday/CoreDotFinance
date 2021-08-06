from coredotfinance.data import BinanceReader

binance = BinanceReader()


def test_binance():
    dataframe = binance.read(
        "ETHBTC", start="2021-03-01", end="2021-03-21", interval="1m"
    )
    assert dataframe.loc["2021-03-01 16:39:00"]["close"][0] == 0.031474
