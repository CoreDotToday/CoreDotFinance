import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def convert_candle_to_dataframe(candle: dict) -> pd.DataFrame:
    # https://towardsdatascience.com/building-a-cryptocurrency-dashboard-using-plotly-and-binance-api-352e7f6f62c9
    df = pd.DataFrame(candle, columns=['일자', '시가', '고가', '저가', '종가', '거래량', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
    df.일자 = pd.to_datetime(df.일자, unit='ms')
    df.거래량 = df.거래량.astype('float64')
    df = df.set_index('일자').sort_index(ascending=False)
    return df.iloc[:, :5]


def make_ohlcv_graph(df: pd.DataFrame, open='시가', high='고가', low='저가', close='종가', volume='거래량') -> None:
    # hovertext 생성
    ohlc_candle_hovertext=[]
    volume_bar_hovertext=[]
    for i in range(len(df[open])):
        ohlc_candle_hovertext.append(f"날짜: {df.index[i].date()}<br>시가: {df[open][i]}<br>고가: {df[high][i]}<br>저가: {df[low][i]}<br>종가: {df[close][i]}")
        volume_bar_hovertext.append(f"날짜: {df.index[i].date()}<br>거래량: {df[volume][i]}")
    # OHLC 캔들 차트 생성
    ohlc_candle = go.Candlestick(
        x=df.index,
        open=df[open], high=df[high], low=df[low], close=df[close],
        text=ohlc_candle_hovertext, hoverinfo='text',
        increasing_line_color='red', decreasing_line_color='blue',
    )
    # 거래량 바 차트 생성
    volume_bar = go.Bar(
        x=df.index,
        y=df[volume],
        text=volume_bar_hovertext, hoverinfo='text',
    )
    # 그래프 그리기
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    fig.add_trace(ohlc_candle, row=1, col=1)
    fig.add_trace(volume_bar, row=2, col=1)
    fig.update_layout(
        yaxis1_title='가격',
        yaxis2_title='거래량',
        xaxis2_title='기간',
        xaxis1_rangeslider_visible=False,
        xaxis2_rangeslider_visible=True,
        showlegend=False,
        yaxis1=dict(domain=[0.25, 1]),
        yaxis2=dict(domain=[0, 0.2]),
    )
    fig.show()