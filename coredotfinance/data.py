import re
import datetime
import warnings

from coredotfinance.krx.api.data_reader import data_reader


class KrxReader:
    """
    krx data를 읽어오는 인스턴스를 생성한다. 많은 양의 데이터를 짧은 시간안에
    불러오게 하면 krx에서 IP를 차단하기 때문에 많은 양의 데이터 읽어오기는
    api 기능을 사용하는 것을 권장한다.

    Parameters
    ----------
    api_key : str
        coredotfinance의 데이터베이스에서 데이터를 받아오기 위해서는
        api_key 설정이 필요하다. api 기능을 사용해서 IP 차단을 피할 수 있다.
    """

    def __init__(
        self,
        api_key=None,
    ):
        self.api_key = api_key

    def _date_check(self, date):
        """
        date 가 None 이면 return 한다. None date 는 today 로 convert 되기 때문이다.
        """
        if date is None:
            return
        if re.match(r'[0-9]{4}-[0-1][0-9]-([0-2][0-9]|3[0-1])', date) is None:
            raise ValueError(f"date is supposed to be 'YYYY-MM-DD and proper date, but {date}")

    def _date_convert(self, date):
        """
        date 가 None 이면 today 를 return 한다.
        """
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
            *,
            start=None,
            end=None,
            kind="stock",
            api=False,
    ):
        """
        data.krx로 부터 금융 데이터를 읽어온다.

        Parameters
        ----------
        symbol : str
            조회하고자 하는 데이터의 종목코드
            형태는 종목과 종류마다 다르다. 예) 삼성전자 : '005930', ARIRANG 200 : '152100'
        start : str
            조회하고자 하는 데이터의 시작일
            형태는 YYYYMMDD가 되어야 한다. 예) 20210601
        end : str
            조회하고자 하는 데이터의 종료일
            형태는 YYYYMMDD가 되어야 한다. 예) 20210601
        kind : str, default "stock"
            조회하고자 하는 데이터의 종류
            데이터의 종류 - krx : ["stock", "etf", "etn", "elw", "per"]
        api : bool, default False
            만얀 api_key가 설정되어 있지 않으면서 api가 True면 error가 발생한다.

        Returns
        -------
        DataFrame
        """

        if start is None or end is None:
            warnings.warn("start or end is None. "
                          "It would lead an error because datetime.datetime.now() is default "
                          "and it could be holiday when stock marker was not held "
                          "or before stock marker is opened")

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

    def read_all(self, date=None, *, kind='stock', api=False):
        """
        Parameters
        ----------
        date : str
            조회하고자 하는 데이터의 조회일
            형태는 YYYYMMDD가 되어야 한다. 예) 20210601
        kind : str, default "stock"
            조회하고자 하는 데이터의 종류
            데이터의 종류 - krx : ["stock", "etf", "etn", "elw", "per"]
        api : bool, default False
           만얀 api_key가 설정되어 있지 않으면서 api가 True면 error가 발생한다.

        Returns
        -------
        DataFrame
        """

        if date is None:
            warnings.warn("date is None. "
                          "It would lead an error because datetime.datetime.now() is default"
                          "and it could be holiday when stock marker was not held "
                          "or before stock marker is opened")

        self._date_check(date)
        date = self._date_convert(date)
        self._kind_check(kind)
        self._api_key_check(api)

        if kind == "stock":
            return data_reader("12001", date=date)
        elif kind == "per":
            # 12021 기능 호출시 종목명 error -> <em class ="up"></em> 가 붙어서 나오는 error
            df = data_reader("12021", search_type="전종목", market='전체', date=date)
            df.replace(' <em class ="up"></em>', '', regex=True, inplace=True)
            return df
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

