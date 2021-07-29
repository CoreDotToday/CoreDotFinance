import pandas as pd
import requests

from coredotfinance.binance import dataframe_util, datetime_util


def request_get_data(symbol, start_timestamp, end_timestamp):
    """Yahoo Finance의 symbol의 History 조회"""
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "referer": "http://m.naver.com",
    }
    params = {
        "includeAdjustedClose": "true",
        "interval": "1d",
        "period1": start_timestamp,
        "period2": end_timestamp,
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def get_ohlcv(
    symbol, *, start=None, end=None, adjust_price=True, real_price=False
) -> pd.DataFrame:
    """Yahoo Finance의 symbol를 활용하여 가격정보(OHLCV) 조회"""
    if start is None:
        start = "19000101"
    if end is None:
        end = datetime_util.get_date_today()

    start_timestamp = datetime_util.convert_date2timestamp_sec(start)
    end_timestamp = datetime_util.convert_date2timestamp_sec(end)
    response = request_get_data(symbol, start_timestamp, end_timestamp)

    timestamp = response["chart"]["result"][0]["timestamp"]
    datetime = datetime_util.convert_timestamp2datetime_list(timestamp)
    open = response["chart"]["result"][0]["indicators"]["quote"][0]["open"]
    high = response["chart"]["result"][0]["indicators"]["quote"][0]["high"]
    low = response["chart"]["result"][0]["indicators"]["quote"][0]["low"]
    close = response["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    adjclose = response["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
    volume = response["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
    df = pd.DataFrame(
        {
            "datetime": datetime,
            "open": open,
            "high": high,
            "low": low,
            "close": close,
            "adj_close": adjclose,
            "volume": volume,
        },
    )

    if adjust_price:
        df = apply_adjust_price(df)
    elif real_price:
        df = apply_real_price(df)

    df = dataframe_util.rename_cols2kor(df)
    df = dataframe_util.set_index_datetime(df)
    return df


def apply_adjust_price(data: pd.DataFrame) -> pd.DataFrame:
    """Yahoo Finance의 수정종가를 활용하여 다른 수정 가격"""
    df = data.copy()
    ratio = df["close"] / df["adj_close"]
    df["adj_open"] = df["open"] / ratio
    df["adj_high"] = df["high"] / ratio
    df["ajd_low"] = df["low"] / ratio
    df["ajd_volume"] = df["volume"] * ratio

    df = df.drop(["open", "high", "low", "close", "volume"], axis=1)

    df = df.rename(
        columns={
            "adj_open": "open",
            "adj_high": "high",
            "ajd_low": "low",
            "adj_close": "close",
            "ajd_volume": "volume",
        },
    )

    df = df[["open", "high", "low", "close", "volume"]]
    return df[["open", "high", "low", "close", "volume"]]


def apply_real_price(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df = df.drop(["adj_close"], axis=1)

    df = df[["open", "high", "low", "close", "volume"]]
    return df[["open", "high", "low", "close", "volume"]]
