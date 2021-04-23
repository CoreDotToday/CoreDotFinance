import sys
import pytest

finance_path = sys.path[0].replace('/test', '')
sys.path.append(finance_path)

from finance.tools import get, per, etf, etn, elw


@pytest.mark.parametrize("stock", [
    (),
    ('KT&G',)
])
def test_get(stock):
    assert get(*stock) is not None