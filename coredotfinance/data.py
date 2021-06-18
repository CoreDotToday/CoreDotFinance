# -*- coding: utf-8 -*-
import os

from pandas import DataFrame

from coredotfinance.krx import KrxReader
from coredotfinance.binance import BinanceReader


class DataReader:
    """Fetches financial data from which parameters indicate.
    Without using API, Data comes from the web by requesting to their server.
    So many times of trial to request in every second in a row would lead IP blocking
    by the website. If bulky data is needed, Using API is highly recommended.

    Parameters
    ----------
    source : str
        "krx" -> data from data.krx.co.kr or data through API
        "binance" -> date from https://www.binance.com or data through API
    api_key : str
        Api_key to fetch data from database on coredotfinance.
        For avoiding IP blocking from web site
    """

    def __init__(self, source, api_key=None):
        expected_source = ["krx", "binance"]
        if source not in expected_source:
            raise ValueError(f"The source, {source} is not expected")
        self.source = source
        self.api_key = api_key

    def get(self, symbol, start, end, kind=None, api=False) -> DataFrame:
        """

        Parameters
        ----------
        symbol : str
            stands for symbol or code which is used to called in the market.
            proper symbol is needed for each source
        start : str
            stands for start date DataReader fetches data from.
            Form has to be "YYYY-MM-DD". For example, "2021-06-17"
        end : str
            stands for end date DataReader fetches data until.
            Form has to be "YYYY-MM-DD". For example, "2021-06-17"
        kind : str, default None
            Some sources need to specify this parameter.
            list of kind:
                krx : ["stock", "etf", "etn", "elw", "per"]
        api : bool, default False
            If api is not set, It will raise error

        Returns
        -------
        DataFrame
        """
        if self.source == "krx":
            return KrxReader(
                symbol=symbol,
                start=start,
                end=end,
                kind=kind,
                api=api,
                api_key=self.api_key,
            ).read()

        elif self.source == "binance":
            return BinanceReader(symbol, start, end, api, self.api_key).read()
