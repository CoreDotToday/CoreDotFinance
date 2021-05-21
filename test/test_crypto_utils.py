from coredotfinance.crypto.utils import date_to_timestamp, get_date_list
from freezegun import freeze_time


def test_date_to_timestamp():
    assert date_to_timestamp("20200420") == "1587308400000"


@freeze_time("20210420")
def test_get_date_list():
    assert get_date_list("20210103") == ["20210420", "20210401", "20210301", "20210201", "20210103"]
