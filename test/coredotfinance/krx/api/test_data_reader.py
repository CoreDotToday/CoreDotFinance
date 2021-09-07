import pytest
from coredotfinance.krx.api.data_reader import data_reader


# No function code
def test_no_function_code():
    with pytest.raises(ValueError):
        data_reader("000000")
