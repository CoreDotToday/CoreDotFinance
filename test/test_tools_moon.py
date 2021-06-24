import pandas as pd
from coredotfinance.krx.api.data_reader import data_reader
from coredotfinance.krx.api.tool import (
    convert_stock_name2ticker,
    convert_stock_ticker2name,
    get_adjusted_price,
    get_df_12009,
    get_stock_info,
    get_stock_pack,
)


def test_convert_stock_name2ticker():
    assert convert_stock_name2ticker("삼성전자") == "005930"


def test_convert_stock_ticker2name():
    assert convert_stock_ticker2name("005930") == "삼성전자"


def test_get_stock_info():
    get_stock_info().시장구분.unique == ["KOSPI", "KOSDAQ"]


def test_get_stock_pack():
    col_12003 = set(data_reader("12003", item="삼성전자").columns)
    col_12021 = set(data_reader("12021", item="삼성전자", search_type="개별추이").columns)
    col_12023 = set(data_reader("12023", item="삼성전자", search_type="개별추이").columns)
    col_12029 = set(get_df_12009("삼성전자").columns)
    col_union = col_12003 | col_12021 | col_12023 | col_12029
    assert col_union.intersection(set(get_stock_pack("삼성전자").columns))


def test_get_df_12009():
    cols = [
        "거래량_기관",
        "거래량_기타법인",
        "거래량_개인",
        "거래량_외국인",
        "거래량_전체",
        "거래대금_기관",
        "거래대금_기타법인",
        "거래대금_개인",
        "거래대금_외국인",
        "거래대금_전체",
    ]
    assert set(cols).intersection(set(get_df_12009("삼성전자").columns))


def test_get_adjusted_price():
    df = pd.DataFrame(
        {
            "종가": [50000, 11000],
            "거래량": [1000, 6000],
            "상장주식수": [100, 500],
        },
        index=["2021-05-21", "2021-05-20"],
    )
    assert get_adjusted_price(df, "종가")[1] == 55000
    assert get_adjusted_price(df, "거래량")[1] == 1200
    assert get_adjusted_price(df, "종가", inplace=True)[1] == df.수정종가[1]
