import datetime
import os
import time

import numpy as np
import pandas as pd

from coredotfinance.binance import dataframe_util, datetime_util

from coredotfinance.binance.api import (
    api_24hr,
    api_avg_price,
    api_depth,
    api_exchange_info,
    api_klines,
)
from coredotfinance.binance.utils import get_date_list


def get_symbols() -> list:
    """Binance의 Symbol List 리턴"""
    response = api_exchange_info()
    symbol_list = [
        response["symbols"][i]["symbol"] for i in range(len(response["symbols"]))
    ]
    return symbol_list


def get_current_price(symbol) -> float:
    """대상 Symbol의 현재 가격 리턴"""
    print(symbol.upper())
    response = api_avg_price(symbol.upper())
    return float(response.get("price"))


def get_orderbook(symbol, limit=None) -> pd.DataFrame:
    """대상 Symbol의 호가창(DataFrame) 리턴"""
    print(symbol.upper())
    response = api_depth(symbol.upper(), limit=limit)
    bids = np.array(response["bids"])
    asks = np.array(response["asks"])
    concat = np.concatenate((bids, asks), axis=1)
    df = pd.DataFrame(
        concat, columns=["bid_price", "bid_volume", "ask_price", "ask_volume"]
    )
    df = dataframe_util.rename_cols2kor(df)
    return df


def get_24hr_all_price() -> pd.DataFrame:
    """모든 Symbol의 24시간 동안의 가격 정보(DataFrame) 리턴 (거래대금순 내림차순 정렬)"""
    response = api_24hr()
    df = pd.DataFrame(response)
    df["tradingValue"] = df["volume"].astype(float) * df["weightedAvgPrice"].astype(
        float
    )
    isUSDT = df["symbol"].str.contains(".USDT", regex=True)
    cols = [
        "symbol",
        "priceChange",
        "priceChangePercent",
        "openPrice",
        "highPrice",
        "lowPrice",
        "lastPrice",
        "volume",
        "tradingValue",
    ]
    df = (
        df.loc[isUSDT, cols]
        .sort_values(by=["tradingValue"], ascending=False)
        .reset_index(drop=True)
    )
    df = dataframe_util.rename_cols2kor(df)
    return df


def get_ohlcv(
    symbol: str = "BTCUSDT", interval="1d", start=None, end=None, limit=1000
) -> pd.DataFrame:
    """대상 symbol의 가격 정보(DataFrame) 리턴

    Parameters
    ----------
    symbol : str, optional
        Binance Symbol, by default "BTCUSDT"
    interval : str, optional
        조회 간격 설정, by default "1d"
        (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
    start : str, optional
        조회 시작 날짜(YYYYMMDD), by default 최근 날짜
    end : str, optional
        조회 끝 날짜(YYYYMMDD), by default 최근 날짜
    limit : int, optional
        조회 개수, by default 1000

    Returns
    -------
    pd.DataFrame
        대상 symbol의 조회 조건에 맞는 일시별 시가/고가/저가/종가/거래량 DataFrame
    """
    if start:
        start = datetime_util.convert_date2timestamp_sec(start) * 1000  # s -> ms
    if end:
        end = datetime_util.convert_date2timestamp_sec(end) * 1000  # s -> ms

    ohlcv = api_klines(symbol.upper(), interval, start, end, limit)

    df = pd.DataFrame(ohlcv).iloc[:, :6]
    df.columns = ["datetime", "open", "high", "low", "close", "volume"]
    df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")

    df = dataframe_util.rename_cols2kor(df)
    df = datetime_util.set_index_datetime(df)

    if "d" in interval or "h" in interval:
        df.tz_localize("UTC")

    print(symbol.upper())
    return df.astype(float)


def get_hourly_ohlcv_to_pickle(symbol_list, start_day, dir):
    """Symbol List에 대해 지정된 시작날짜부터의 1시간 간격 가격정보(OHLCV)를 지정된 폴더에 pickle 파일로 저장"""
    date_list = get_date_list(start_day)
    for symbol in symbol_list:
        outdir = f"{dir}/binance/pickles_{symbol}"  # Symbol 별로 폴더 분류
        if not os.path.exists(outdir):  # 폴더가 존재하지 않을경우 폴더 생성
            os.makedirs(outdir)
        for idx, date in enumerate(date_list):
            if not idx == 0:  # idx==0이면, idx-1==-1이 되므로 제외
                start, end = date_list[idx], date_list[idx - 1]
                df = get_ohlcv(symbol, interval="1h", start=start, end=end, limit=1000)
                if df.shape[0] == 0:  # DataFrame에 Data가 없는 경우 For Loop 종료
                    print(f"NoData : {symbol.upper()}_{date[:-2]}")
                    break
                df.to_pickle(f"{outdir}/{symbol}_{date[:-2]}.pickle")
                time.sleep(1)  # API에서 IP Ban 방지하기 위하여 1초 Delay


def get_recent_ohlcv_to_pickle(symbol_list, dir):
    """Symbol List에 대해 전일 기준 해당월의 1시간 간격 가격정보(OHLCV)를 지정된 폴더에 pickle 파일로 저장"""
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    first_day = datetime.datetime(yesterday.year, yesterday.month, 1).strftime("%Y%m%d")
    for symbol in symbol_list:
        outdir = f"{dir}/binance/pickles_{symbol}"  # Symbol 별로 폴더 분류
        if not os.path.exists(outdir):  # 폴더가 존재하지 않을경우 폴더 생성
            os.makedirs(outdir)
        df = get_ohlcv(symbol, interval="1h", start=first_day)
        df.to_pickle(f"{outdir}/{symbol}_{first_day[:-2]}.pickle")
        time.sleep(1)  # API에서 IP Ban 방지하기 위하여 1초 Delay
