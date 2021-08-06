import os

from coredotfinance.data import KrxReader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
api_key_file = os.path.join(BASE_DIR, "apikey.txt")
with open(api_key_file, "r") as f:
    apikey = f.read().strip()

krx = KrxReader(apikey)


def test_krx_read():
    dataframe = krx.read(
        symbol="000660", start="2021-07-20", end="2021-07-20", api=True
    )
    assert dataframe["close"][0] == 118500


def test_krx_read_date():
    dataframe = krx.read_date(date="2021-07-20", api=True)
    assert dataframe["close"][0] == 3075


def test_krx_stock_adjust():
    dataframe = krx.read(
        "035720", start="2021-04-14", end="2021-04-15", adjust=True, api=True
    )
    assert dataframe.loc["2021-04-14"]["close"] == 111600
