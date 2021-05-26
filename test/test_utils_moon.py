from datetime import datetime, timezone

from coredotfinance._utils import (
    _convert_date2timestamp,
    _convert_timestamp2datetime_list,
    _get_past_days_ago,
    _get_today,
)
from freezegun import freeze_time


@freeze_time("20210420")
def test_get_today():
    assert _get_today() == "20210420"


@freeze_time("20210420")
def test_get_past_days_ago():
    assert _get_past_days_ago(10) == "20210410"


def test_convert_date2timestamp():
    assert _convert_date2timestamp("20200420") == 1587308400


def test_convert_timestamp2datetime_list():
    assert _convert_timestamp2datetime_list([1587308400]) == [datetime(2020, 4, 20)]
