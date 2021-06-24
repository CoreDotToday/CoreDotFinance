from datetime import date, datetime, timedelta

import pytz

UTC = pytz.utc


def convert_date2timestamp_sec(date: str) -> str:
    """Date(YYYYMMDD) -> UTC Timestamp(in seconds)"""
    year, month, day = int(date[0:4]), int(date[4:6]), int(date[6:8])
    timestamp = datetime(year, month, day, tzinfo=UTC).timestamp()
    return int(timestamp)


def convert_timestamp2datetime_list(timestamp_list: list()) -> list():
    datetime_list = [datetime.fromtimestamp(timestamp) for timestamp in timestamp_list]
    return datetime_list


def get_date_today() -> str:
    """Get date of today(YYYYMMDD)"""
    today = date.today()
    return today.strftime("%Y%m%d")


def get_date_past_days_ago(days: int = 365) -> str:
    """Get date of past days ago"""
    today = date.today()
    past_days_ago = today - timedelta(days)
    return past_days_ago.strftime("%Y%m%d")

