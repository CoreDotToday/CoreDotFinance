import pandas as pd
import requests
from coredotfinance._utils import (
    _convert_date2timestamp,
    _convert_timestamp2datetime_list,
    _get_today,
)


def request_get_data(ticker, start_timestamp, end_timestamp):
    """Yahoo Finance의 Ticker의 History 조회"""
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
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


def get_ohlcv(ticker, *, start=None, end=None, adjust_price=True, real_price=False) -> pd.DataFrame:
    """Yahoo Finance의 Ticker를 활용하여 가격정보(OHLCV) 조회"""
    if start is None:
        start = "19000101"
    if end is None:
        end = _get_today()

    start_stamp = _convert_date2timestamp(start)
    end_stamp = _convert_date2timestamp(end)
    response = request_get_data(ticker, start_stamp, end_stamp)

    timestamp = response["chart"]["result"][0]["timestamp"]
    datetime = _convert_timestamp2datetime_list(timestamp)
    open = response["chart"]["result"][0]["indicators"]["quote"][0]["open"]
    high = response["chart"]["result"][0]["indicators"]["quote"][0]["high"]
    low = response["chart"]["result"][0]["indicators"]["quote"][0]["low"]
    close = response["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    adjclose = response["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
    volume = response["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
    df = (
        pd.DataFrame(
            {
                "일자": datetime,
                "시가": open,
                "고가": high,
                "저가": low,
                "종가": close,
                "수정종가": adjclose,
                "거래량": volume,
            },
        )
        .set_index("일자")
        .sort_index(ascending=False)
    )

    if adjust_price:
        df = apply_adjust_price(df)
    elif real_price:
        df = apply_real_price(df)

    return df


def apply_adjust_price(data: pd.DataFrame) -> pd.DataFrame:
    """Yahoo Finance의 수정종가를 활용하여 다른 수정 가격"""
    df = data.copy()
    ratio = df["종가"] / df["수정종가"]
    df["수정시가"] = df["시가"] / ratio
    df["수정고가"] = df["고가"] / ratio
    df["수정저가"] = df["저가"] / ratio
    df["수정거래량"] = df["거래량"] * ratio

    df = df.drop(["시가", "고가", "저가", "종가", "거래량"], axis=1)

    df.rename(
        columns={"수정시가": "시가", "수정고가": "고가", "수정저가": "저가", "수정종가": "종가", "수정거래량": "거래량"},
        inplace=True,
    )

    df = df[["시가", "고가", "저가", "종가", "거래량"]]
    return df[["시가", "고가", "저가", "종가", "거래량"]]


def apply_real_price(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df = df.drop(["수정종가"], axis=1)

    df = df[["시가", "고가", "저가", "종가", "거래량"]]
    return df[["시가", "고가", "저가", "종가", "거래량"]]
