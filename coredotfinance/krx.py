import pandas as pd

from coredotfinance._krx import read


class KrxReader:
    """
    Returns DataFrame of korean financial data from data.krx.co.kr.
    Trying to get bulky data through many times of iteration leads IP blocking.
    So using api to get bulky data is highly recommended

    Parameters
    ----------
    symbol : str
        stands for stock symbol which is used to called in Korean stock market.
        Proper symbol is needed for each source.
    start : str
        stands for start date DataReader fetches data from.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"
    end : str
        stands for end date DataReader fetches data until.
        Form has to be "YYYY-MM-DD". For example, "2021-06-17"
    kind : str, default "stoack"
        Some sources need to specify this parameter.
        list of kind:
            krx : ["stock", "etf", "etn", "elw", "per"]
    api : bool, default False
        If api is not set, It will raise error
    api_key : str
        Api_key to fetch data from database on coredotfinance.
        For avoiding IP blocking from web site.
    """

    def __init__(
        self,
        symbol,
        start,
        end,
        kind="stock",
        api=False,
        api_key=None,
    ):
        expected_kind = ["stock", "etf", "etn", "elw", "per"]

        if kind not in expected_kind:
            raise ValueError(f"The kind, {kind} is not expected")

        if api_key is None and api is not False:
            raise ValueError("api_key has to be set to use api")

        if api is True:
            pass

        self.symbol = symbol
        self.start = start
        self.end = end
        self.kind = kind
        self.api = api
        self.api_key = api_key

    def read(self):

        if self.kind == "stock":
            read_function = read.stock
        elif self.kind == "per":
            read_function = read.per
        elif self.kind == "etf":
            read_function = read.etf
        elif self.kind == "etn":
            read_function = read.etn
        elif self.kind == "elw":
            read_function = read.elw
        else:
            read_function = None
            raise ValueError(f"Check {self.kind} is not in the list of expected_kind")

        return read_function(symbol=self.symbol, start=self.start, end=self.end)
