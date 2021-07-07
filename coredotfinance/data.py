import re
import datetime
import warnings

from coredotfinance.krx.core.krx_website.info import Info
from coredotfinance.krx.api.data_reader import data_reader
from coredotfinance.binance import binance
from coredotfinance.database import krx_db


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

    not_service_api = ["etf", "etn", "elw", "per"]

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

        Parameters
        ----------

        date : str
            YYYY-MM-DD

        Returns
        --------
        str
            YYYYMMDD
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

    def search(self, find, kind='stock'):
        """
        필요 주식의 종목코드 또는 종목명을 검색한다.

        Parameters
        ----------
        find : str
            종목명 또는 종목코드

        Returns
        -------
        tuple
            종목명, 종목코드, 종목코드약식

        Examples
        --------
        from coredotfinance.data import KrxReader
        krx = KrxReader()
        krx.search('삼성전자')

        >>> ('삼성전자', 'KR7005930003', '005930')
        """
        return Info(None, None, None).autocomplete(find, kind)

    def read(
            self,
            symbol,
            *,
            start=None,
            end=None,
            kind="stock",
            api=False
    ):
        """
        해당 주식 가격 데이터를 시작일(start) 부터 종료일(end) 까지 읽어온다.

        Parameters
        ----------
        symbol : str
            조회하고자 하는 데이터의 종목코드.
            형태는 종목과 종류마다 다르다. 예) 삼성전자 : '005930', ARIRANG 200 : '152100'
        start : str
            조회하고자 하는 데이터의 시작일.
            형태는 YYYY-MM-DD가 되어야 한다. 예) 2021-06-01
        end : str
            조회하고자 하는 데이터의 종료일.
            형태는 YYYY-MM-DD가 되어야 한다. 예) 2021-06-01
        kind : str, default "stock"
            조회하고자 하는 데이터의 종류.
            데이터의 종류 - krx : ["stock", "etf", "etn", "elw", "per"]
        api : bool, default False
            api_key가 설정되어 있지 않으면서 api가 True면 error가 발생한다.
            api 이용은 주식 가격만 가능하다.

        Returns
        -------
        pd.DataFrame
            data
        """

        if start is None or end is None:
            warnings.warn("""start or end is None. 
                          It would lead an error because datetime.datetime.now() is default 
                          and it could be holiday when stock marker was not held 
                          or before stock marker is opened""")

        if api and kind in KrxReader.not_service_api:
            raise ValueError(f"{kind} does not service api yet.")

        self._date_check(start)
        self._date_check(end)
        start_8_digit = self._date_convert(start)
        end_8_digit = self._date_convert(end)
        self._kind_check(kind)
        self._api_key_check(api)

        if start_8_digit > end_8_digit:
            raise ValueError(f"start has to be earlier than end, but {start}, {end}")

        if api:
            return krx_db.read(symbol, start, end, kind=kind, resource='krx', api_key=self.api_key)

        if kind == "stock":
            return data_reader("12003", symbol=symbol, start=start_8_digit, end=end_8_digit, kind=kind)
        elif kind == "per":
            return data_reader("12021", symbol=symbol, start=start_8_digit, end=end_8_digit, kind=kind, search_type="개별추이")
        elif kind == "etf":
            return data_reader("13103", symbol=symbol, start=start_8_digit, end=end_8_digit, kind=kind)
        elif kind == "etn":
            return data_reader("13203", symbol=symbol, start=start_8_digit, end=end_8_digit, kind=kind)
        elif kind == "elw":
            return data_reader('13302', symbol=symbol, start=start_8_digit, end=end_8_digit, kind=kind)
        else:
            raise ValueError(f"Check {kind} is not in the list of expected_kind")

    def read_all(
            self,
            symbol,
            *,
            kind="stock",
            api=False
    ):
        """
        전기간의 해당 주식 가격 데이터를 읽어온다.

        Parameters
        ----------
        symbol : str
            조회하고자 하는 데이터의 종목코드.
            형태는 종목과 종류마다 다르다. 예) 삼성전자 : '005930', ARIRANG 200 : '152100'
        start : str
            조회하고자 하는 데이터의 시작일.
            형태는 YYYY-MM-DD가 되어야 한다. 예) 2021-06-01
        end : str
            조회하고자 하는 데이터의 종료일.
            형태는 YYYY-MM-DD가 되어야 한다. 예) 2021-06-01
        kind : str, default "stock"
            조회하고자 하는 데이터의 종류.
            krx : ["stock", "etf", "etn", "elw", "per"]
        api : bool, default False
            api_key가 설정되어 있지 않으면서 api가 True면 error가 발생한다.
            api 이용은 주식가격만 가능하다.

        Returns
        -------
        pd.DataFrame
            data
        """
        return self.read(symbol, start='1900-01-01', end='2030-01-01', kind=kind, api=api)

    def read_date(self, date=None, *, kind='stock', api=False):
        """
        해당 일자의 전 종목 주식 데이터를 불러온다.

        Parameters
        ----------
        date : str
            조회하고자 하는 데이터의 조회일.
            형태는 YYYY-MM-DD가 되어야 한다. 예) 2021-06-01
        kind : str, default "stock"
            조회하고자 하는 데이터의 종류.
            데이터의 종류 - krx : ["stock", "etf", "etn", "elw", "per"]
        api : bool, default False
           api_key가 설정되어 있지 않으면서 api가 True면 error가 발생한다.

        Returns
        -------
        pd.DataFrame
            data
        """

        if api and kind in KrxReader.not_service_api:
            raise ValueError(f"{kind} does not service api yet.")

        if date is None:
            warnings.warn("""date is None.
                          It would lead an error because datetime.datetime.now() is default 
                          and it could be holiday when stock marker was not held 
                          or before stock marker is opened""")

        self._date_check(date)
        date_8_digit = self._date_convert(date)
        self._kind_check(kind)
        self._api_key_check(api)

        if api:
            return krx_db.read_date(date, kind=kind, resource='krx', api_key=self.api_key)

        if kind == "stock":
            return data_reader("12001", date=date_8_digit, kind=kind)
        elif kind == "per":
            df = data_reader("12021", search_type="전종목", market='전체', date=date_8_digit)
            # 12021 기능 호출시 종목명 <em class ="up"></em> 가 붙어서 나오는 문제를 해결하기 위함
            df.replace(' <em class ="up"></em>', '', regex=True, inplace=True)
            return df
        elif kind == "etf":
            return data_reader("13101", date=date_8_digit, kind=kind)
        elif kind == "etn":
            return data_reader("13201", date=date_8_digit, kind=kind)
        elif kind == "elw":
            return data_reader('13301', date=date_8_digit, kind=kind)
        else:
            raise ValueError(f"Check {kind} is not in the list of expected_kind")


class BinanceReader:
    """
        Returns DataFrame of crypto currency price data from binance.com
        Trying to get bulky data through many times of iteration leads IP blocking.
        So using api to get bulky data is highly recommended.
    """

    def __init__(
            self,
            api_key=None,
    ):
        self.api_key = api_key

    @property
    def symbols(self):
        return binance.get_symbols()

    def read(self, symbol, start, end, interval):
        """
        해당 암호화폐의 가격 데이터를 불러온다.

        Parameters
        ----------
        symbol : str, optional
            Binance Symbol
        interval : str, optional
            조회 간격 설정, by default "1d"
            (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
        start : str, optional
            조회 시작 날짜(YYYY-MM-DD), by default 최근 날짜
        end : str, optional
            조회 끝 날짜(YYYY-MM-DD), by default 최근 날짜

        Returns
        -------
        pd.DataFrame
            data
        """

        start = start.replace('-', '')
        end = end.replace('-', '')

        return binance.get_ohlcv(symbol=symbol, start=start, end=end, interval=interval)