_cols_kor = {
    "symbol": "종목코드",
    "datetime": "일시",
    "open": "시가",
    "high": "고가",
    "low": "저가",
    "close": "종가",
    "volume": "거래량",
    "priceChange": "대비",
    "priceChangePercent": "등락률",
    "lastPrice": "종가",
    "openPrice": "시가",
    "highPrice": "고가",
    "lowPrice": "저가",
    "tradingValue": "거래대금",
    "bid_price": "매수호가",
    "bid_volume": "매수물량",
    "ask_price": "매도호가",
    "ask_volume": "매도물량",
    "adjopen": "수정시가",
    "adjhigh": "수정고가",
    "adjlow": "수정저가",
    "adjclose": "수정종가",
    "adjvolume": "수정거래량",
}


def rename_cols2kor(df):
    df = df.rename(columns=_cols_kor)
    return df
