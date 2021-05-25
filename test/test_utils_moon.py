from coredotfinance.krx.utils_moon import get_today, get_past_days_ago
from freezegun import freeze_time


@freeze_time("20210420")
def test_get_today():
    assert get_today() == '20210420'


@freeze_time("20210420")
def test_get_past_days_ago():
    assert get_past_days_ago(10) == '20210410'
