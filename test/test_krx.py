from coredotfinance.data import KrxReader

krx = KrxReader()


# read check
def test_krx_read():
    dataframe = krx.read(symbol="000660", start="2021-07-20", end="2021-07-20")
    assert dataframe["close"][0] == 118500


# read_date check
def test_krx_read_date():
    dataframe = krx.read_date(date="2021-07-20")
    assert dataframe["close"][0] == 3075


# adjust check
def test_krx_stock_adjust():
    dataframe = krx.read("035720", start="2021-04-14", end="2021-04-15", adjust=True)
    assert dataframe.loc["2021-04-14"]["close"][0] == 111600


# multi index check
def test_krx_etf_read():
    dataframe = krx.read("152100", kind="etf", start="2021-04-15", end="2021-04-16")
    assert dataframe.loc["2021-04-15"]["close"][0] == 44275


# multi index adjust check
def test_krx_etf_adjust():
    dataframe = krx.read(
        "152100", kind="etf", start="2021-04-15", end="2021-04-16", adjust=True
    )
    assert dataframe.loc["2021-04-15"]["close"][0] == 45566


# division parameter check
def test_krx_other_index():
    dataframe = krx.read(
        "에너지", kind="other_index", start="2021-04-15", end="2021-04-16", division="선물지수"
    )
    assert dataframe.loc["2021-04-15"]["close"][0] == 1890.33


# per check
def test_krx_per_read():
    dataframe = krx.read(
        '000660', kind='per', start='2021-04-15', end='2021-04-16'
    )
    assert dataframe.loc["2021-04-15"]["close"][0] == 137500

