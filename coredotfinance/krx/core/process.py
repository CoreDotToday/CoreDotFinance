# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime

second_column_map = {
    "BND_CLSS_NM1": "구분1",  # <- row map
    "BND_CLSS_NM2": "구분2",  # <- row map
}

no_display_columns = [
    "IND_TP_CD",
    "IDX_IND_CD",
    "MKT_ID",
    "CONV_OBJ_TP_CD",
    "ISU_ABBRV_STR",
    "ETF_ISU_CD",
    "BND_CLSS_CD",
    "NUSUAL_ISU_COND_CONTN",
    "KRW_FLUC_TP_CD",
    "OZ_FLUC_TP_CD",
    "FLUC_TP",
    "ISU_ABBRV",
    "SUB_IDX_IND_NM",
    "ISU_CD",
]


def get_dataframe(krx_data, column_map):
    _check_data_validation(krx_data)
    column_map.update(second_column_map)
    data = _apply_column_map(krx_data, column_map)
    data = _date_to_index(data)
    column_data = [column.split("//") for column in data.columns]
    columns_depth = max([len(c) for c in column_data])
    if not _single_column(columns_depth):
        column_data = _remove_same_named_column(column_data, columns_depth)
        columns = _multi_columnize(column_data)
        data.columns = columns
    data = _dataframe_astype(data)

    return data


def _check_data_validation(krx_data):
    if len(list(krx_data.values())[0]) == 0:
        raise Exception("No data, Check parameters")


def _apply_column_map(data_json, column_map):
    readable_column_list = []
    data_list = list(data_json.values())[0]

    for data in data_list:
        readable_column = {}
        for column, data_value in data.items():
            try:
                readable_column[column_map[column]] = data_value
            except:
                if column in no_display_columns or "TP_CD" in column:
                    continue
                else:
                    readable_column[column] = data_value
        readable_column_list.append(readable_column)
    return pd.json_normalize(readable_column_list)


def _date_to_index(data):
    if "일자" not in data.columns:
        # '일자' 열이 있는지 확인
        return data
    if len(data) != len(set(data["일자"].values)):
        # '일자' 가 중복되는 데이터인지 확인
        return data

    date_list = [datetime.strptime(date, "%Y/%m/%d") for date in data["일자"]]
    data.index = date_list
    return data.drop(["일자"], axis="columns")


def _single_column(columns_depth):
    # columns 가 single 인 경우
    if columns_depth == 1:
        return True


def _remove_same_named_column(column_data, columns_depth):
    # 같은 이름으로 multi columnize 되는 것을 방지
    for i in column_data:
        for _ in range(columns_depth - len(i)):
            i.append("")
    return column_data


def _multi_columnize(column_data):
    return np.array(column_data).T.tolist()


def _dataframe_astype(dataframe: pd.DataFrame):
    dataframe = _remove_punctuation(dataframe)
    column_data_type = _get_column_data_type(dataframe)
    dataframe = _0_to_empty_str(dataframe, column_data_type)
    return _data_type_as(dataframe, column_data_type)


def _remove_punctuation(dataframe: pd.DataFrame):
    dataframe.replace(",", "", regex=True, inplace=True)
    dataframe.replace("\-$", "0", regex=True, inplace=True)
    dataframe.replace("", "0", regex=True, inplace=True)

    return dataframe


def _get_column_data_type(dataframe: pd.DataFrame):
    """
    Returns
    -------
        when krx.read_date(date='2021-06-22')

        {'종목명': 'str',
         '시장구분': 'str',
         '소속부': 'str',
         '종가': 'np.int64',
         '대비': 'np.int64',
         '등락률': 'float',
         '시가': 'np.int64',
         '고가': 'np.int64',
         '저가': 'np.int64',
         '거래량': 'np.int64',
         '거래대금': 'np.int64',
         '시가총액': 'np.int64',
         '상장주식수': 'np.int64'}

         또는

        when krx.read('152100', start = '2012-01-01', end='2012-02-01', kind='etf')

         {('종가', ''): 'np.int64',
         ('대비', ''): 'np.int64',
         ('등락률', ''): 'float',
         ('지표가치(IV)', ''): 'float',
         ('시가', ''): 'np.int64',
         ('고가', ''): 'np.int64',
         ('저가', ''): 'np.int64',
         ('거래량', ''): 'np.int64',
         ('거래대금', ''): 'np.int64',
         ('시가총액', ''): 'np.int64',
         ('지표가치총액', ''): 'np.int64',
         ('상장증권수', ''): 'np.int64',
         ('기초지수', '지수명'): 'str',
         ('기초지수', '종가'): 'float',
         ('기초지수', '대비'): 'float',
         ('기초지수', '등락률'): 'float'}
    """
    column_data_type = {}

    for column in dataframe.columns:
        if column in ["종목코드", ("종목코드", "")]:
            continue
        for data in dataframe[column]:
            if data == "" or data == "0":
                continue
            try:
                data = eval(data)
            except:
                # 문자가 들어있는 str은 eval이 작동하지 못한다. ex) 3S, KOSDAQ, 중견기업부
                pass
            data_type = type(data)

            if data_type is str:
                column_data_type[column] = "str"
                break
            elif data_type is int:
                column_data_type[column] = "np.int64"
                break
            elif data_type is float:
                column_data_type[column] = "float"
                break

    return column_data_type


def _0_to_empty_str(dataframe: pd.DataFrame, column_data_type: dict):
    """
    데이터가 str인 column에 들어있는 0을 '' 로 바꾸어 준다.
    column_data_type 에서 value가 'str' 인 column 만 바꾸어 준다.
    """
    for column, datatype in column_data_type.items():
        if datatype == "str":
            dataframe[column].replace("0", "", inplace=True)
    return dataframe


def _data_type_as(dataframe: pd.DataFrame, column_data_type: dict):
    """
    모든 데이터가 str으로 들어가 있는 dateframe을 column_data_type에 담겨있는 정보에 따라서
    데이터의 type을 바꾸어 준다.
    소수로 이루어져 있는 데이터는 str -> float
    정수로 이루어져 있는 데이터는 str -> np.int64

    Parameters
    ----------
    dataframe
    column_data_type

    Returns
    -------

    """
    for column, datatype in column_data_type.items():
        if datatype == "str":
            continue
        try:
            dataframe = dataframe.astype({column: eval(datatype)})
        except ValueError:
            # 햔 column에 int와 float이 같이 들어있는 경우가 있다. 그때!! 바로!! 쓴다!!
            dataframe = dataframe.astype({column: float})
    return dataframe
