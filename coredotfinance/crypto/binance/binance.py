import os
import time
import pandas as pd
import numpy as np
from coredotfinance.crypto.binance.api import api_exchange_info, api_avg_price, api_depth, api_24hr, api_klines
from coredotfinance.crypto.utils import date_to_timestamp, get_date_list


def get_tickers() -> list:
    response = api_exchange_info()
    ticker_list = [response["symbols"][i]["symbol"] for i in range(len(response["symbols"]))]
    return ticker_list


def get_current_price(ticker) -> float:
    print(ticker.upper())
    response = api_avg_price(ticker.upper())
    return float(response.get("price"))


def get_orderbook(ticker, limit=None) -> pd.DataFrame:
    print(ticker.upper())
    response = api_depth(ticker.upper(), limit=limit)
    bids = np.array(response["bids"])
    asks = np.array(response["asks"])
    concat = np.concatenate((bids, asks), axis=1)
    df = pd.DataFrame(concat, columns=["매수가격", "매수수량", "매도가격", "매도수량"])
    df.index = df.index.tz_localize("UTC").tz_convert("Asia/Seoul")
    return df


def get_market_detail(ticker=None) -> dict:
    if ticker is None:
        response = api_24hr()
    else:
        print(ticker.upper())
        response = api_24hr(ticker.upper())
    return response


def get_24hrs() -> pd.DataFrame:
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
        df.loc[isUSDT]
        .loc[:, cols.keys()]
        .rename(columns=cols)
        .sort_values(by=["거래대금"], ascending=False)
        .reset_index(drop=True)
    )
    return df


def get_ohlcv(ticker: str = "BTCUSDT", interval="1d", start=None, end=None, limit=None) -> pd.DataFrame:
    print(ticker.upper())
    if start:
        start = date_to_timestamp(start)
    if end:
        end = date_to_timestamp(end)
    ohlcv = api_klines(ticker.upper(), interval, start, end, limit)
    df = pd.DataFrame(
        ohlcv,
        columns=[
            "일자",
            "시가",
            "고가",
            "저가",
            "종가",
            "거래량",
            "closeTime",
            "quoteAssetVolume",
            "numberOfTrades",
            "takerBuyBaseVol",
            "takerBuyQuoteVol",
            "ignore",
        ],
    )
    df.일자 = pd.to_datetime(df.일자, unit="ms")
    df.거래량 = df.거래량.astype("float64")
    df = df.set_index("일자").sort_index(ascending=False).iloc[:, :5]
    df.index = df.index.tz_localize("UTC").tz_convert("Asia/Seoul")
    return df


def get_hourly_ohlcv_to_pickle(ticker_list, start_day):
    date_list = get_date_list(start_day)
    for ticker in ticker_list:
        outdir = f"./pickles_{ticker}"  # Ticker 별로 폴더 분류
        if not os.path.exists(outdir):  # 폴더가 존재하지 않을경우 폴더 생성
            os.mkdir(outdir)
        for idx, date in enumerate(date_list):
            if not idx == 0:  # idx==0이면, idx-1==-1이 되므로 제외
                start, end = date_list[idx], date_list[idx - 1]
                df = get_ohlcv(ticker, interval="1h", start=start, end=end, limit=1000)
                if df.shape[0] == 0:  # DataFrame에 Data가 없는 경우 For Loop 종료
                    print(f"NoData : {ticker.upper()}_{date[:-2]}")
                    break
                df.to_pickle(f"{outdir}/{ticker}_{date[:-2]}.pickle")
                time.sleep(1)  # API에서 IP Ban 방지하기 위하여 1초 Delay
