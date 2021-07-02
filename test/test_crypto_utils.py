from coredotfinance.binance.utils import get_date_list
from freezegun import freeze_time


@freeze_time("20210420")
def test_get_date_list():
    assert get_date_list("20210103") == [
        "20210420",
        "20210401",
        "20210301",
        "20210201",
        "20210103",
    ]
