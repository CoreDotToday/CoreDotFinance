import os
import datetime
import time
import pandas as pd
import numpy as np
from coredotfinance.crypto.binance.api import (
    api_exchange_info,
    api_avg_price,
    api_depth,
    api_24hr,
    api_klines,
)
from coredotfinance.crypto.utils import get_date_list
from coredotfinance._utils import _convert_date2timestamp


def get_tickers() -> list:
    """Binance의 Ticker List 리턴"""
    response = api_exchange_info()
    ticker_list = [response["symbols"][i]["symbol"] for i in range(len(response["symbols"]))]
    return ticker_list


def get_current_price(ticker) -> float:
    """대상 Ticker의 현재 가격 리턴"""
    print(ticker.upper())
    response = api_avg_price(ticker.upper())
    return float(response.get("price"))


def get_orderbook(ticker, limit=None) -> pd.DataFrame:
    """대상 Ticker의 호가창(DataFrame) 리턴"""
    print(ticker.upper())
    response = api_depth(ticker.upper(), limit=limit)
    bids = np.array(response["bids"])
    asks = np.array(response["asks"])
    concat = np.concatenate((bids, asks), axis=1)
    df = pd.DataFrame(concat, columns=["매수가격", "매수수량", "매도가격", "매도수량"])
    return df


def get_24hr_all_price() -> pd.DataFrame:
    """모든 Ticker의 24시간 동안의 가격 정보(DataFrame) 리턴 (거래대금순 내림차순 정렬)"""
    response = api_24hr()
    df = pd.DataFrame(response)
    df["tradingValue"] = df["volume"].astype(float) * df["weightedAvgPrice"].astype(float)
    isUSDT = df.symbol.str.contains(".USDT", regex=True)
    cols = {
        "symbol": "종목코드",
        "priceChange": "대비",
        "priceChangePercent": "등락률",
        "lastPrice": "종가",
        "openPrice": "시가",
        "highPrice": "고가",
        "lowPrice": "저가",
        "volume": "거래량",
        "tradingValue": "거래대금",
    }
    df = (
        df.loc[isUSDT, cols.keys()]
        .rename(columns=cols)
        .sort_values(by=["거래대금"], ascending=False)
        .reset_index(drop=True)
    )
    return df


def get_ohlcv(
    ticker: str = "BTCUSDT", interval="1d", start=None, end=None, limit=None
) -> pd.DataFrame:
    """대상 Ticker의 가격 정보(DataFrame) 리턴

    Parameters
    ----------
    ticker : str, optional
        Binance Ticker, by default "BTCUSDT"
    interval : str, optional
        조회 간격 설정, by default "1d"
        (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
    start : str, optional
        조회 시작 날짜(YYYYMMDD), by default 최근 날짜
    end : str, optional
        조회 끝 날짜(YYYYMMDD), by default 최근 날짜
    limit : int, optional
        조회 개수, by default 500

    Returns
    -------
    pd.DataFrame
        대상 Ticker의 조회 조건에 맞는 일시별 시가/고가/저가/종가/거래량 DataFrame
    """
    print(ticker.upper())
    if start:
        start = _convert_date2timestamp(start) * 1000  # s -> ms
    if end:
        end = _convert_date2timestamp(end) * 1000  # s -> ms
    ohlcv = api_klines(ticker.upper(), interval, start, end, limit)
    df = pd.DataFrame(ohlcv).iloc[:, :6]
    df.columns = ["일시", "시가", "고가", "저가", "종가", "거래량"]
    df.일시 = pd.to_datetime(df.일시, unit="ms")
    df.거래량 = df.거래량.astype("float64")
    df = df.set_index("일시").sort_index(ascending=False)
    return df


def get_hourly_ohlcv_to_pickle(ticker_list, start_day, dir):
    """Ticker List에 대해 지정된 시작날짜부터의 1시간 간격 가격정보(OHLCV)를 지정된 폴더에 pickle 파일로 저장"""
    date_list = get_date_list(start_day)
    for ticker in ticker_list:
        outdir = f"{dir}/binance/pickles_{ticker}"  # Ticker 별로 폴더 분류
        if not os.path.exists(outdir):  # 폴더가 존재하지 않을경우 폴더 생성
            os.makedirs(outdir)
        for idx, date in enumerate(date_list):
            if not idx == 0:  # idx==0이면, idx-1==-1이 되므로 제외
                start, end = date_list[idx], date_list[idx - 1]
                df = get_ohlcv(ticker, interval="1h", start=start, end=end, limit=1000)
                if df.shape[0] == 0:  # DataFrame에 Data가 없는 경우 For Loop 종료
                    print(f"NoData : {ticker.upper()}_{date[:-2]}")
                    break
                df.to_pickle(f"{outdir}/{ticker}_{date[:-2]}.pickle")
                time.sleep(1)  # API에서 IP Ban 방지하기 위하여 1초 Delay


def get_recent_ohlcv_to_pickle(ticker_list, dir):
    """Ticker List에 대해 전일 기준 해당월의 1시간 간격 가격정보(OHLCV)를 지정된 폴더에 pickle 파일로 저장"""
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    first_day = datetime.datetime(yesterday.year, yesterday.month, 1).strftime("%Y%m%d")
    for ticker in ticker_list:
        outdir = f"{dir}/binance/pickles_{ticker}"  # Ticker 별로 폴더 분류
        if not os.path.exists(outdir):  # 폴더가 존재하지 않을경우 폴더 생성
            os.makedirs(outdir)
        df = get_ohlcv(ticker, interval="1h", start=first_day)
        df.to_pickle(f"{outdir}/{ticker}_{first_day[:-2]}.pickle")
        time.sleep(1)  # API에서 IP Ban 방지하기 위하여 1초 Delay
