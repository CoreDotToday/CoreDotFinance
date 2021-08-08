import re
import datetime
import warnings

from coredotfinance.krx.core.krx_website.info import Info
from coredotfinance.krx.api.data_reader import data_reader
from coredotfinance.binance import binance
from coredotfinance.database import krx_db
from coredotfinance.krx.core import option


class KrxReader:
    """
    krx data를 읽어오는 인스턴스를 생성한다. 
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
        if re.match(r"[0-9]{4}-[0-1][0-9]-([0-2][0-9]|3[0-1])", date) is None:
            raise ValueError(
                f"date is supposed to be 'YYYY-MM-DD and proper date, but {date}"
            )

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
        return date.replace("-", "")

    def _kind_check(self, kind):
        expected_kind = ["stock", "etf", "etn", "elw", "per", "index", "other_index"]
        if kind not in expected_kind:
            raise ValueError(f"expected kind in {expected_kind}, but got {kind}")

    def _api_key_check(self, api):
        if self.api_key is None and api is not False:
            raise ValueError("api_key has to be set in order to use api")

    def search(self, find, kind="stock", **kwargs):
        """
        필요 주식의 종목코드 또는 종목명을 검색한다.

        Parameters
        ----------
        find : str
            종목명 또는 종목코드

        kind : str
            조회하고자 하는 데이터의 종류\n
            krx : ['stock', 'etf', 'index' ,'per', 'index', 'other_index']

        kwargs:
            division : str
                조회하고자 하는 데이터의 세부 구분

        Returns
        -------
        tuple
            종목명, 종목코드, 종목코드약식


        Examples
        --------
        >>> from coredotfinance.data import KrxReader
        >>> krx = KrxReader()
        >>> krx.search('삼성전자')

        >>> ('삼성전자', 'KR7005930003', '005930')
        """
        return Info(None, None, None).autocomplete(find, kind, **kwargs)

    def read(self, symbol, *, start=None, end=None, kind="stock", api=False, **kwargs):
        """
        해당 주식 가격 데이터를 시작일(start) 부터 종료일(end) 까지 읽어온다.

        Parameters
        ----------
        symbol : str
            조회하고자 하는 데이터의 종목코드.\n
            형태는 종목과 종류마다 다르다.\n
            예) 삼성전자 : '005930', ARIRANG 200 : '152100'
        start : str
            조회하고자 하는 데이터의 시작일.\n
            형태는 YYYY-MM-DD가 되어야 한다. \n
            예) 2021-06-01
        end : str
            조회하고자 하는 데이터의 종료일.\n
            형태는 YYYY-MM-DD가 되어야 한다.\n
            예) 2021-06-01
        kind : str, default "stock"
            조회하고자 하는 데이터의 종류.\n
            krx : ['stock', 'etf', 'index' ,'per', 'index', 'other_index']
        kwargs :
            division : str
                조회하고자 하는 데이터의 세부 구분\n
                other_index : ['선물지수', '옵션지수', '전략지수', '상품지수']
            reverse : bool, default false
                dataframe을 거꾸로 정렬하기
            kor : bool, default false
                columns를 한글로 받아오기
            adjust : bool, default false
                수정주가 적용하기

        Returns
        -------
        pd.DataFrame
            data


        Examples
        -------
        >>> from coredotfinance.data import KrxReader
        >>> krx = KrxReader()
        >>> dataframe = krx.read('000660', start='2021-07-01')
        """

        if start is None or end is None:
            warnings.warn(
                """start or end is None. 
                          It would lead an error because datetime.datetime.now() is default 
                          and it could be holiday when stock marker was not held 
                          or before stock marker is opened"""
            )

        if api and kind in KrxReader.not_service_api:
            raise ValueError(f"{kind} does not service api yet.")

        self._date_check(start)
        self._date_check(end)
        start_8_digit = self._date_convert(start)
        end_8_digit = self._date_convert(end)
        self._kind_check(kind)
        self._api_key_check(api)
        self.division = kwargs.get('division', '').upper()

        if start_8_digit > end_8_digit:
            raise ValueError(f"start has to be earlier than end, but {start}, {end}")

        if api:
            dataframe = krx_db.read(
                symbol, start, end, kind=kind, resource="krx", api_key=self.api_key
            )
        elif kind == "stock":
            dataframe = data_reader(
                "12003",
                symbol=symbol,
                start=start_8_digit,
                end=end_8_digit,
                kind=kind,
                **kwargs,
            )
        elif kind == "per":
            dataframe = data_reader(
                "12021",
                symbol=symbol,
                start=start_8_digit,
                end=end_8_digit,
                kind=kind,
                search_type="개별추이",
                **kwargs,
            )
        elif kind == "etf":
            dataframe = data_reader(
                "13103",
                symbol=symbol,
                start=start_8_digit,
                end=end_8_digit,
                kind=kind,
                **kwargs,
            )
        elif kind == "etn":
            dataframe = data_reader(
                "13203",
                symbol=symbol,
                start=start_8_digit,
                end=end_8_digit,
                kind=kind,
                **kwargs,
            )
        elif kind == "elw":
            dataframe = data_reader(
                "13302",
                symbol=symbol,
                start=start_8_digit,
                end=end_8_digit,
                kind=kind,
                **kwargs,
            )
        elif kind == "index":
            dataframe = data_reader(
                "11003",
                symbol=symbol,
                start=start_8_digit,
                end=end_8_digit,
                kind=kind,
                **kwargs,
            )
        elif kind == "other_index":
            dataframe = data_reader(
                "11012",
                symbol=symbol,
                start=start_8_digit,
                end=end_8_digit,
                kind=kind,
                **kwargs,
            )

        else:
            raise ValueError(f"Check {kind} is not in the list of expected_kind")

        return option.options(dataframe=dataframe, **kwargs)

    def read_all(self, symbol, *, kind="stock", api=False, **kwargs):
        """
        전기간의 해당 주식 가격 데이터를 읽어온다.

        Parameters
        ----------
        symbol : str
            조회하고자 하는 데이터의 종목코드.\n
            형태는 종목과 종류마다 다르다.\n
            예) 삼성전자 : '005930', ARIRANG 200 : '152100'
        kind : str, default "stock"
            조회하고자 하는 데이터의 종류.\n
            krx : ["stock", "etf", "etn", "elw", "per"]
        kwargs :
            kind : str
                조회하고자 하는 데이터의 종류\n
                krx : ['stock', 'etf', 'index' ,'per', 'index', 'other_index']
            division : str
                조회하고자 하는 데이터의 세부 구분\n
                other_index : ['선물지수', '옵션지수', '전략지수', '상품지수']
            reverse : bool, default false
                dataframe을 거꾸로 정렬하기
            kor : bool, default false
                columns를 한글로 받아오기
            adjust : bool, default false
                수정주가 적용하기

        Returns
        -------
        pd.DataFrame
            data


        Examples
        -------
        >>> from coredotfinance.data import KrxReader
        >>> krx = KrxReader()
        >>> dataframe = krx.read_all('000660')
        """

        if api:
            dataframe = krx_db.read_all(
                symbol, kind=kind, resource="krx", api_key=self.api_key
            )
        else:
            dataframe = self.read(
                symbol, start="1900-01-01", end="2030-01-01", kind=kind, **kwargs
            )

        return dataframe

    def read_date(self, date=None, *, kind="stock", api=False, **kwargs):
        """
        해당 일자의 전 종목 주식 데이터를 불러온다.

        Parameters
        ----------
        date : str
            조회하고자 하는 데이터의 조회일.\n
            형태는 YYYY-MM-DD가 되어야 한다.\n
            예) 2021-06-01
        kind : str, default "stock"
            조회하고자 하는 데이터의 종류.\n
            krx : ['stock', 'etf', 'index' ,'per', 'index', 'other_index']
        kwargs :
            division : str
                조회하고자 하는 데이터의 세부 구분\n
                other_index : ['선물지수', '옵션지수', '전략지수', '상품지수']
            reverse : bool, default false
                dataframe을 거꾸로 정렬하기
            kor : bool, default false
                columns를 한글로 받아오기
            adjust : bool, default false
                수정주가 적용하기

        Returns
        -------
        pd.DataFrame
            data


        Examples
        -------
        >>> from coredotfinance.data import KrxReader
        >>> krx = KrxReader()
        >>> dataframe = krx.read_date('2021-07-20')
        """

        if api and kind in KrxReader.not_service_api:
            raise ValueError(f"{kind} does not service api yet.")

        if date is None:
            warnings.warn(
                """date is None.
                          It would lead an error because datetime.datetime.now() is default 
                          and it could be holiday when stock marker was not held 
                          or before stock marker is opened"""
            )

        self._date_check(date)
        date_8_digit = self._date_convert(date)
        self._kind_check(kind)
        self._api_key_check(api)

        if api:
            dataframe = krx_db.read_date(
                date, kind=kind, resource="krx", api_key=self.api_key
            )
        elif kind == "stock":
            dataframe = data_reader("12001", date=date_8_digit, kind=kind)
        elif kind == "per":
            df = data_reader("12021", search_type="전종목", market="전체", date=date_8_digit)
            # 12021 기능 호출시 종목명 <em class ="up"></em> 가 붙어서 나오는 문제를 해결하기 위함
            df.replace(' <em class ="up"></em>', "", regex=True, inplace=True)
            dataframe = df
        elif kind == "etf":
            dataframe = data_reader("13101", date=date_8_digit, kind=kind)
        elif kind == "etn":
            dataframe = data_reader("13201", date=date_8_digit, kind=kind)
        elif kind == "elw":
            dataframe = data_reader("13301", date=date_8_digit, kind=kind)
        elif kind == "index":
            dataframe = data_reader("11001", date=date_8_digit, kind=kind, **kwargs)
        elif kind == "other_index":
            dataframe = data_reader("11010", date=date_8_digit, kind=kind, **kwargs)
        else:
            raise ValueError(f"Check {kind} is not in the list of expected_kind")

        if kwargs.get('adjust', None) is True:
            warnings.warn('data from read_date can not be adjusted')
            del kwargs['adjust']

        return option.options(dataframe, **kwargs)


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

    def symbol_list(self):
        return binance.get_symbols()

    def interval_list(self):
        return ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

    def read(self, symbol, start, end, interval, **kwargs):
        """
        해당 암호화폐의 가격 데이터를 불러온다.

        Parameters
        ----------
        symbol : str
            조회하고자 하는 데이터의 코인코드.\n
            예) 이더리움 : 'ETHBTC'
        interval : str
            조회 간격 설정
            (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
        start : str
            조회하고자 하는 데이터의 시작일.\n
            형태는 YYYY-MM-DD가 되어야 한다. \n
            예) 2021-06-01
        end : str
            조회하고자 하는 데이터의 종료일.\n
            형태는 YYYY-MM-DD가 되어야 한다.\n
            예) 2021-06-01

        Returns
        -------
        pd.DataFrame
            data
        """

        start = start.replace("-", "")
        end = end.replace("-", "")

        dataframe = binance.get_ohlcv(symbol=symbol, start=start, end=end, interval=interval)
        return option.options(dataframe, **kwargs)
