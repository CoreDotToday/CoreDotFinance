import os
import configparser
import requests
import pandas as pd


def load_api_key() -> str:
    path = os.path.dirname(os.path.realpath(__file__))
    config = configparser.ConfigParser()
    config.read_file(open(path + "/key.cfg"))
    API_KEY = config.get("BINANCE", "BINANCE_API_KEY")
    return API_KEY


def get_data_from_api(api: str, payload: dict = None) -> dict:
    url = "https://api.binance.com"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "referer": "http://m.naver.com",
        "X-MBX-APIKEY": load_api_key(),
    }
    response = requests.get(f"{url}{api}", headers=headers, params=payload)
    return response.json()


def get_kline_candlestick_data(ticker, interval, startTime, endTime, limit) -> dict:
    """
    Return Examples
    1499040000000,      // Open time  -> GMT 기준 long type timestamp
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
    """
    api = "/api/v3/klines"
    payload = {
        "symbol": ticker,
        "interval": interval,
        "limit": limit,
        "startTime": startTime,
        "endTime": endTime,
    }
    return get_data_from_api(api, payload)


def convert_candle_to_dataframe(candle: dict) -> pd.DataFrame:
    # https://towardsdatascience.com/building-a-cryptocurrency-dashboard-using-plotly-and-binance-api-352e7f6f62c9
    df = pd.DataFrame(
        candle,
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
    df = df.set_index("일자").sort_index(ascending=False)
    return df.iloc[:, :5]


def get_tickers():
    api = "/api/v3/exchangeInfo"
    response = get_data_from_api(api)
    ticker_list = [
        response["symbols"][i]["symbol"] for i in range(len(response["symbols"]))
    ]
    print(ticker_list)
    return ticker_list