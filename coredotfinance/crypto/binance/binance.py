import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from coredotfinance.crypto.binance.api import *
from coredotfinance.crypto.utils import date_to_timestamp


def get_tickers() -> list:
    response = api_exchange_info()
    ticker_list = [
        response["symbols"][i]["symbol"] for i in range(len(response["symbols"]))
    ]
    print(ticker_list)
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
    df["tPrice"] = df["volume"].astype(float) * df["weightedAvgPrice"].astype(float)
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
    }
    df = (
        df.loc[isUSDT]
        .sort_values(by=["tPrice"], ascending=False)
        .reset_index(drop=True)
        .loc[:, cols.keys()]
        .rename(columns=cols)
    )
    return df


def get_ohlcv(
    ticker: str = "BTCBUSD", interval="1d", start=None, end=None, limit=None
) -> pd.DataFrame:
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
    return df


def make_ohlcv_graph(
    df: pd.DataFrame, open="시가", high="고가", low="저가", close="종가", volume="거래량"
) -> None:
    # hovertext 생성
    ohlc_candle_hovertext = []
    volume_bar_hovertext = []
    for i in range(len(df[open])):
        ohlc_candle_hovertext.append(
            f"날짜: {df.index[i].date()}<br>시가: {df[open][i]}<br>고가: {df[high][i]}<br>저가: {df[low][i]}<br>종가: {df[close][i]}"
        )
        volume_bar_hovertext.append(f"날짜: {df.index[i].date()}<br>거래량: {df[volume][i]}")
    # OHLC 캔들 차트 생성
    ohlc_candle = go.Candlestick(
        x=df.index,
        open=df[open],
        high=df[high],
        low=df[low],
        close=df[close],
        text=ohlc_candle_hovertext,
        hoverinfo="text",
        increasing_line_color="red",
        decreasing_line_color="blue",
    )
    # 거래량 바 차트 생성
    volume_bar = go.Bar(
        x=df.index,
        y=df[volume],
        text=volume_bar_hovertext,
        hoverinfo="text",
    )
    # 그래프 그리기
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    fig.add_trace(ohlc_candle, row=1, col=1)
    fig.add_trace(volume_bar, row=2, col=1)
    fig.update_layout(
        yaxis1_title="가격",
        yaxis2_title="거래량",
        xaxis2_title="기간",
        xaxis1_rangeslider_visible=False,
        xaxis2_rangeslider_visible=True,
        showlegend=False,
        yaxis1=dict(domain=[0.25, 1]),
        yaxis2=dict(domain=[0, 0.2]),
    )
    fig.show()
