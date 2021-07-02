from datetime import datetime, timedelta

from coredotfinance.binance.api import api_check_server_time
from coredotfinance.binance.binance import (
    get_24hr_all_price,
    get_current_price,
    get_ohlcv,
    get_orderbook,
    get_symbols,
)
from coredotfinance.binance.utils import get_date_list
from freezegun import freeze_time


# crypto.binance.api.py
def test_api_check_server_time():
    time_api = datetime.fromtimestamp(int(api_check_server_time()["serverTime"]) / 1000)
    time_now = datetime.now()
    assert (time_api - time_now) < timedelta(seconds=1)


# crypto.binance.binance.py
def test_get_symbols():
    assert len(get_symbols()) > 0


def test_get_current_price():
    assert get_current_price("BTCUSDT") > 0


def test_get_orderbook():
    assert len(get_orderbook("BTCUSDT")) > 0


def test_24hr_all_price():
    df = get_24hr_all_price()
    assert len(df) > 0
    assert df["거래대금"].max() == df["거래대금"][0]


def test_get_ohlcv_klines():
    df = get_ohlcv("BTCUSDT")
    assert len(df) > 0
    assert df.columns.tolist() == ["시가", "고가", "저가", "종가", "거래량"]


@freeze_time("20210420")
def test_get_date_list():
    assert get_date_list("20210103") == [
        "20210420",
        "20210401",
        "20210301",
        "20210201",
        "20210103",
    ]
