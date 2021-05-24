import requests
import pandas as pd
from coredotfinance._utils import _convert_date2timestamp, _convert_timestamp2datetime_list, _get_today, _get_past_days_ago


def request_get_data(ticker, start_timestamp, end_timestamp):
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "referer": "http://m.naver.com",
    }
    params = {
        "includeAdjustedClose": "true",
        "interval": "1d",
        "period1": start_timestamp,
        "period2": end_timestamp,
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def get_ohlcv(ticker, start=_get_past_days_ago(), end=_get_today()):
    start_stamp = _convert_date2timestamp(start)
    end_stamp = _convert_date2timestamp(end)
    response = request_get_data(ticker, start_stamp, end_stamp)
    timestamp = response["chart"]["result"][0]["timestamp"]
    datetime = _convert_timestamp2datetime_list(timestamp)
    open = response["chart"]["result"][0]["indicators"]["quote"][0]["open"]
    high = response["chart"]["result"][0]["indicators"]["quote"][0]["high"]
    low = response["chart"]["result"][0]["indicators"]["quote"][0]["low"]
    close = response["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    adjclose = response["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
    volume = response["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
    df = (
        pd.DataFrame(
            {
                "일자": datetime,
                "시가": open,
                "고가": high,
                "저가": low,
                "종가": close,
                "수정종가": adjclose,
                "거래량": volume,
            },
        )
        .set_index("일자")
        .sort_index(ascending=False)
    )
    return df


print(get_ohlcv("^KS11"))
