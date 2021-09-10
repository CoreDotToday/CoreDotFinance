import pytest
from coredotfinance.krx.api.data_reader import data_reader


# No function code
def test_no_function_code():
    with pytest.raises(ValueError):
        data_reader("000000")


def test_code_no_string():
    with pytest.raises(ValueError):
        data_reader(
            12003,
            symbol="000660",
            start="20210907",
            end="20210907",
        )
