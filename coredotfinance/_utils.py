from datetime import date, datetime, timedelta

import pytz

from coredotfinance.language_kor import _cols_kor

# datetime

UTC = pytz.utc


def _convert_date2timestamp_sec(date: str) -> str:
    """Date(YYYYMMDD) -> UTC Timestamp(in seconds)"""
    year, month, day = int(date[0:4]), int(date[4:6]), int(date[6:8])
    timestamp = datetime(year, month, day, tzinfo=UTC).timestamp()
    return int(timestamp)


def _convert_timestamp2datetime_list(timestamp_list: list()) -> list():
    datetime_list = [datetime.fromtimestamp(timestamp) for timestamp in timestamp_list]
    return datetime_list


def _get_date_today() -> str:
    """Get date of today(YYYYMMDD)"""
    today = date.today()
    return today.strftime("%Y%m%d")


def _get_date_past_days_ago(days: int = 365) -> str:
    """Get date of past days ago"""
    today = date.today()
    past_days_ago = today - timedelta(days)
    return past_days_ago.strftime("%Y%m%d")


# dataframe


def _rename_cols2kor(df):
    df = df.rename(columns=_cols_kor)
    return df


def _set_index_datetime(df):
    if "datetime" in df:
        df = df.set_index("datetime").sort_index(ascending=False)
    elif "일시" in df:
        df = df.set_index("일시").sort_index(ascending=False)
    return df
