import sys
import pytest

# finance_path = sys.path[0].replace('/test', '')
# sys.path.append(finance_path)

from finance.tools import get, per, etf, etn, elw


@pytest.mark.parametrize("stock", [
    (),
    ('naver', 20210428, 20210428)
])
def test_get(stock):
    assert get(*stock) is not None


@pytest.mark.parametrize("stock", [
    (),
    ('naver', 20210428, 20210428)
])
def test_per(stock):
    assert per(*stock) is not None


@pytest.mark.parametrize("ETF",[
    (),
    ('arirang', 20210428, 20210428)
])
def test_etf(ETF):
    assert etf(*ETF) is not None


@pytest.mark.parametrize("ETN",[
    (),
    ('qv 건설', 20210428, 20210428)
])
def test_etn(ETN):
    assert etn(*ETN) is not None


@pytest.mark.parametrize("ELW",[
    (),
    ('KBF937삼성전자콜', 20210428, 20210428)
])
def test_elw(ELW):
    assert elw(*ELW) is not None
