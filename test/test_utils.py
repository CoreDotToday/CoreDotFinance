import pytest

from coredotfinance.krx.utils import classifier, start_end_validation, week_day


def test_classifier():
    pass


@pytest.mark.parametrize(
    "good_ex",
    [
        (None, None),
        (20210420, None),  # from start to 60 days later
        (20210420, 20210423),  # 4 biz days
        (20210420, 20210420),  # a biz day
    ],
)
def test_start_end_validation_good(good_ex):
    assert start_end_validation(*good_ex)


@pytest.mark.parametrize(
    "bad_ex",
    [
        (2021042, 20210423),  # wrong start len is under 8-digit
        (20210420, 2021042),  # wrong end len is under 8-digit
        (20210423, 20210420),  # start > end
        (20210333, 20210413),  # day is out of range of month
    ],
)
def test_start_end_validation_bad(bad_ex):
    try:
        if start_end_validation(*bad_ex):
            raise Exception("test Fail")
    except Exception:
        pass  # test passed


def test_week_day():
    assert 4 == week_day("20210423")


@pytest.mark.parametrize(
    "item_name",
    [
        ("3s",),
        ("AJ네트웍스",),
        ("ARIRANG 200",),
        ("KB 레버리지 S&P 500 선물 ETN(H)",),
        ("KBF937삼성전자콜", "elw"),
    ],
)
def test_classifier_item_name(item_name):
    assert "item name" == classifier(*item_name)


@pytest.mark.parametrize(
    "item_code", [("211270",), ("00104K",), ("58F937", "elw"), ("58FK37", "elw")]
)
def test_classifier_item_code(item_code):
    assert "item code" == classifier(*item_code)
