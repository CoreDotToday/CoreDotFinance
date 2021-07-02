import configparser
import os

import requests


def load_api_key() -> str:
    """Binance API 키를 key.cfg에서 불러온다."""
    path = os.path.dirname(os.path.realpath(__file__))
    config = configparser.ConfigParser()
    config.read_file(open(path + "/key.cfg"))
    API_KEY = config.get("BINANCE", "BINANCE_API_KEY")
    return API_KEY


def get_data_from_api(api: str, payload: dict = None) -> dict:
    """Get 방식으로 Binance API에 요청"""
    url = "https://api.binance.com"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "referer": "http://m.naver.com",
    }
    response = requests.get(f"{url}{api}", headers=headers, params=payload)
    return response.json()


def api_check_server_time() -> dict:
    """Binance API 요청(Check Server Time)"""
    api = "/api/v3/time"
    response = get_data_from_api(api)
    return response


def api_exchange_info() -> dict:
    """Binance API 요청(Exchange Information)"""
    api = "/api/v3/exchangeInfo"
    response = get_data_from_api(api)
    return response


def api_depth(symbol, limit=None) -> dict:
    """Binance API 요청(Order Book)"""
    api = "/api/v3/depth"
    payload = {
        "symbol": symbol,
        "limit": limit,
    }
    response = get_data_from_api(api, payload)
    return response


def api_avg_price(symbol) -> dict:
    """Binance API 요청(Current Average Price)"""
    api = "/api/v3/avgPrice"
    payload = {
        "symbol": symbol,
    }
    response = get_data_from_api(api, payload)
    return response


def api_24hr(symbol=None) -> dict:
    """Binance API 요청(24hr symbol Price Change Statistics)"""
    api = "/api/v3/ticker/24hr"
    payload = {
        "symbol": symbol,
    }
    response = get_data_from_api(api, payload)
    return response


def api_klines(symbol, interval, startTime, endTime, limit) -> dict:
    """Binance API 요청(Kline/Candlestick Data)
    Klines are uniquely identified by their open time.
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
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "startTime": startTime,
        "endTime": endTime,
    }
    response = get_data_from_api(api, payload)
    return response
