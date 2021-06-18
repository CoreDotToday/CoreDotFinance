
class BinanceReader:
    """
        Returns DataFrame of crypto currency price data from binance.com
        Trying to get bulky data through many times of iteration leads IP blocking.
        So using api to get bulky data is highly recommended.

        Parameters
        ----------
        ticker : str
            stands for symbol or code which is used to called in the market.
            proper ticker is needed for each source
        start : str
            stands for start date DataReader fetches data from.
            Form has to be "YYYY-MM-DD". For example, "2021-06-17"
        end : str
            stands for end date DataReader fetches data until.
            Form has to be "YYYY-MM-DD". For example, "2021-06-17"
        api : bool, default False
            If api is not set, It will raise error.
        api_key : str
            Api_key to fetch data from database on coredotfinance.
            For avoiding IP blocking from web site

    """
    def __init__(
            self,
            ticker,
            start,
            end,
            api,
            api_key
    ):

        if api_key is None and api is not False:
            raise ValueError("api_key has to be set to use api")

        if api is True:
            pass

