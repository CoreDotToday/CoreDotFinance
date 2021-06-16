import datetime

import pandas as pd
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots


def get_date_list(start_day) -> list:
    """시작일부터 오늘까지를 1달 간격으로 나눈 것을 리스트로 만듦"""
    date_list = []
    start = datetime.datetime.strptime(start_day, "%Y%m%d")
    today = datetime.datetime.now()
    first_day = datetime.datetime(today.year, today.month, 1)
    date_list.append(today.strftime("%Y%m%d"))
    date = first_day
    delta = relativedelta(months=1)
    while date > start:
        date_list.append(date.strftime("%Y%m%d"))
        date = date - delta
    date_list.append(start.strftime("%Y%m%d"))
    return date_list


def make_ohlcv_graph(
    df: pd.DataFrame, open="시가", high="고가", low="저가", close="종가", volume="거래량"
) -> None:
    # hovertext 생성
    ohlc_candle_hovertext = []
    volume_bar_hovertext = []
    for i in range(len(df[open])):
        ohlc_candle_hovertext.append(
            f"일자: {df.index[i].date()}<br>시가: {df[open][i]}<br>고가: {df[high][i]}<br>저가: {df[low][i]}<br>종가: {df[close][i]}"
        )
        volume_bar_hovertext.append(f"일자: {df.index[i].date()}<br>거래량: {df[volume][i]}")
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
