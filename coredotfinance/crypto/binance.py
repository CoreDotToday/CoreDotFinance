import os
import configparser
import requests


def get_data_from_api(api: str, payload: dict=None) -> dict:
    url = 'https://api.binance.com'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0',
        'referer': 'http://m.naver.com',
        'X-MBX-APIKEY': load_api_key(),
    }
    response = requests.get(f'{url}{api}', headers=headers, params=payload)
    return response.json()


def load_api_key() -> str:
    path = os.path.dirname(os.path.realpath(__file__))
    config = configparser.ConfigParser()
    config.read_file(open(path + '/key.cfg'))
    API_KEY = config.get('BINANCE', 'BINANCE_API_KEY')
    return API_KEY


def get_kline_candlestick_data(ticker: str='BTCUSDT', interval: str='1d', startTime=None, endTime=None, limit: int=1000,) -> dict:
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
    api = '/api/v3/klines'
    payload={'symbol': ticker, 'interval': interval, 'limit': limit, 'startTime': startTime, 'endTime': endTime}
    return get_data_from_api(api, payload)


def get_tickers():
    api = '/api/v3/exchangeInfo'
    response = get_data_from_api(api)
    ticker_list = [response['symbols'][i]['symbol'] for i in range(len(response['symbols']))]
    print(ticker_list)

