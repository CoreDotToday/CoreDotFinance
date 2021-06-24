import pytest
from datetime import datetime
import pandas as pd
import numpy as np

from coredotfinance.krx.core import process


@pytest.fixture
def example_data_json():
    return {
        "output": [
            {
                "TRD_DD": "2021/04/26",
                "TDD_CLSPRC": "375,500",
                "FLUC_TP_CD": "2",
                "CMPPREVDD_PRC": "-2,500",
                "FLUC_RT": "-0.66",
                "TDD_OPNPRC": "376,500",
                "TDD_HGPRC": "379,000",
                "TDD_LWPRC": "375,500",
                "ACC_TRDVOL": "167,042",
                "ACC_TRDVAL": "62,964,265,000",
                "MKTCAP": "61,680,904,822,500",
                "LIST_SHRS": "164,263,395",
            }
        ],
        "CURRENT_DATETIME": "2021.04.26 AM 10:57:43",
    }


@pytest.fixture
def example_column_map():
    return {
        "TRD_DD": "일자",
        "TDD_CLSPRC": "종가",
        "CMPPREVDD_PRC": "대비",
        "FLUC_RT": "등락률",
        "TDD_OPNPRC": "시가",
        "TDD_HGPRC": "고가",
        "TDD_LWPRC": "저가",
        "ACC_TRDVOL": "거래량",
        "ACC_TRDVAL": "거래대금",
        "MKTCAP": "시가총액",
        "LIST_SHRS": "상장주식수",
        "BND_CLSS_NM1": "구분1",
        "BND_CLSS_NM2": "구분2",
    }


def test_check_data_validation(example_data_json):
    try:
        process.check_data_validation(example_data_json)
        test = True
    except Exception:
        test = False
    assert test


def test_check_data_validation_wrong():
    no_data = {"output": [], "CURRENT_DATETIME": "2021.04.26 AM 10:57:43"}
    try:
        process.check_data_validation(no_data)
        test = False
    except Exception:
        test = True
    assert test


def test_apply_column_map(example_data_json, example_column_map):
    test = list(process.apply_column_map(example_data_json, example_column_map))
    answer = ["일자", "종가", "대비", "등락률", "시가", "고가", "저가", "거래량", "거래대금", "시가총액", "상장주식수"]
    assert test == answer


def test_date_to_index():
    test_data = pd.DataFrame([["2021/04/21", "100"]], columns=["일자", "주가"])
    assert process.date_to_index(test_data).index[0] == datetime(2021, 4, 21)


def test_date_to_index_wrong():
    test_data = pd.DataFrame(
        [["2021/04/21", "100"], ["2021/04/21", "120"]], columns=["일자", "주가"]
    )
    assert process.date_to_index(test_data).index[0] == 0


def test_remove_same_named_column():
    test_data_1 = [["종가"], ["대비"], ["등락률", "주가"]]
    test_data_2 = [["종가", ""], ["대비", ""], ["등락률", "주가"]]
    assert process.remove_same_named_column(test_data_1, 2) == test_data_2


def test_multi_columnize():
    test_data_1 = [["종가", ""], ["대비", ""], ["등락률", "주가"]]
    test_data_2 = [["종가", "대비", "등락률"], ["", "", "주가"]]
    assert process.multi_columnize(test_data_1, 2) == test_data_2


def test_string_to_float():
    test_data = pd.DataFrame(
        [["100,000", "삼성", "-", "1000", "1000.33", 1, 1000.33]],
        columns=["주가", "str", "-", "int_str", "float_str", "int", "float"],
    )
    assert list(process.string_to_float(test_data).loc[0]) == [
        100000.0,
        "삼성",
        np.nan,
        1000.0,
        1000.33,
        1,
        1000.33,
    ]
