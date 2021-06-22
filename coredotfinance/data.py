import re
import datetime

from coredotfinance.krx import read
from coredotfinance.krx.data_reader import data_reader



class KrxReader:
    """
    Returns DataFrame of korean financial data from data.krx.co.kr.
    Trying to get bulky data through many times of iteration leads IP blocking.
    So using api to get bulky data is highly recommended

    Parameters
    ----------
    api_key : str
        Api_key to fetch data from database on coredotfinance.
        For avoiding IP blocking from web site.
    """

    def __init__(
        self,
        api_key=None,
    ):
        self.api_key = api_key

    def _date_check(self, date):
        if date is None:
            return
        if re.match(r'[0-9]{4}-[0-1][0-9]-([0-2][0-9]|3[0-1])', date) is None:
            raise ValueError(f"date is supposed to be 'YYYY-MM-DD and proper date, but {date}")

    def _date_convert(self, date):
        today = str(datetime.datetime.now().date())
        if date is None:
            date = today
        return date.replace('-', '')

    def _kind_check(self, kind):
        expected_kind = ["stock", "etf", "etn", "elw", "per"]
        if kind not in expected_kind:
            raise ValueError(f"expected kind in {expected_kind}, but got {kind}")

    def _api_key_check(self, api):
        if self.api_key is None and api is not False:
            raise ValueError("api_key has to be set in order to use api")

    def read(
            self,
            symbol,
            start=None,
            end=None,
            kind="stock",
            api=False,
    ):
        """

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
        kind : str, default "stock"
            Some sources need to specify this parameter.
            list of kind:
                krx : ["stock", "etf", "etn", "elw", "per"]
        api : bool, default False
            If api is not set, It will raise error

        Returns
        -------
        DataFrame
        """

        self._date_check(start)
        self._date_check(end)
        start = self._date_convert(start)
        end = self._date_convert(end)
        self._kind_check(kind)
        self._api_key_check(api)

        if start > end:
            raise ValueError(f"start has to be earlier than end, but {start}, {end}")

        if kind == "stock":
            return data_reader("12003", symbol=symbol, start=start, end=end, kind=kind)
        elif kind == "per":
            return data_reader("12021", symbol=symbol, start=start, end=end, kind=kind, search_type="개별추이")
        elif kind == "etf":
            return data_reader("13103", symbol=symbol, start=start, end=end, kind=kind)
        elif kind == "etn":
            return data_reader("13203", symbol=symbol, start=start, end=end, kind=kind)
        elif kind == "elw":
            return data_reader('13302', symbol=symbol, start=start, end=end, kind=kind)
        else:
            raise ValueError(f"Check {kind} is not in the list of expected_kind")

    def read_all(self, date=None, kind='stock', api=False):
        """
        Parameters
        ----------
        date : str
            stands for the date DataReader fetches for.
            Form has to be "YYYY-MM-DD". For example, "2021-06-17"
        kind : str, default "stock"
            Some sources need to specify this parameter.
            list of kind:
                krx : ["stock", "etf", "etn", "elw", "per"]
        api : bool, default False
            If api is not set, It will raise error
        Returns
        -------
        DataFrame
        """
        self._date_check(date)
        date = self._date_convert(date)
        self._kind_check(kind)
        self._api_key_check(api)

        if kind == "stock":
            return data_reader("12001", date=date)
        elif kind == "per":
            return data_reader("12021", search_type="전종목", market='전체', data=date)
        elif kind == "etf":
            return data_reader("13101", date=date, kind=kind)
        elif kind == "etn":
            return data_reader("13201", date=date, kind=kind)
        elif kind == "elw":
            return data_reader('13301', date=date, kind=kind)
        else:
            raise ValueError(f"Check {kind} is not in the list of expected_kind")

class BinanceReader:
    """
        Returns DataFrame of crypto currency price data from binance.com
        Trying to get bulky data through many times of iteration leads IP blocking.
        So using api to get bulky data is highly recommended.
    """
    def __init__(self):
        pass

