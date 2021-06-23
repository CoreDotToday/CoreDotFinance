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


class GettingDataNm:
    _data_nm = None

    @property
    def data_nm(self):
        item_name = GettingDataNm._data_nm
        GettingDataNm._data_nm = None
        return item_name

    @data_nm.setter
    def data_nm(self, item_name):
        GettingDataNm._data_nm = item_name


def data_nm_column(data):
    item_name = GettingDataNm().data_nm
    if item_name is None:
        return data
    data["종목명"] = [item_name for _ in range(len(data))]

    return data


def get_dataframe(krx_data, column_map):
    check_data_validation(krx_data)
    column_map.update(second_column_map)
    data = apply_column_map(krx_data, column_map)
    data = date_to_index(data)
    column_data = [column.split("//") for column in data.columns]
    columns_depth = max([len(c) for c in column_data])
    if not single_column(columns_depth):
        column_data = remove_same_named_column(column_data, columns_depth)
        columns = multi_columnize(column_data, columns_depth)
        data.columns = columns
    # 00data = string_to_float(data)
    data = dataframe_astype(data)

    # data = data_nm_column(data)
    return data


def check_data_validation(krx_data):
    if len(list(krx_data.values())[0]) == 0:
        raise Exception("No data, Check parameters")


def apply_column_map(data_json, column_map):
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


def date_to_index(data):
    if "일자" not in data.columns:
        # '일자' 열이 있는지 확인
        return data
    if len(data) != len(set(data["일자"].values)):
        # '일자' 가 중복되는 데이터인지 확인
        return data

    date_list = [datetime.strptime(date, "%Y/%m/%d") for date in data["일자"]]
    data.index = date_list
    return data.drop(["일자"], axis="columns")


def single_column(columns_depth):
    # columns 가 single 인 경우
    if columns_depth == 1:
        return True


def remove_same_named_column(column_data, columns_depth):
    # 같은 이름으로 multi columnize 되는 것을 방지
    for i in column_data:
        for _ in range(columns_depth - len(i)):
            i.append("")
    return column_data


def multi_columnize(column_data, columns_depth):
    columns = []
    # column 만들기
    for i in range(1, columns_depth + 1):
        layer = []
        for column in column_data:
            layer.append(column[:i][-1])
        columns.append(layer)

    return columns


def string_to_float(data: pd.DataFrame):
    new_values = []
    for column in data.columns:
        series = data[column]
        edited_values = []
        number_data = True
        for i in series:
            try:
                value = i.replace(",", "")
                float(value)
            except:
                # 값이 비어있는 경우
                if i != "-":
                    number_data = False
                    break
                else:
                    value = 0
            if '.' in value:
                value = np.float32(value)
            else:
                value = np.int64(value)
            edited_values.append(value)
        if number_data:
            new_values.append(edited_values)
        else:
            new_values.append(series.array)

    return pd.DataFrame(np.array(new_values).T, columns=data.columns, index=data.index)


def dataframe_astype(dataframe: pd.DataFrame):
    dataframe = remove_punctuation(dataframe)
    column_data_type = get_column_data_type(dataframe)
    return data_type_as(dataframe, column_data_type)


def remove_punctuation(dataframe: pd.DataFrame):
    dataframe.replace(',', '', regex=True, inplace=True)
    dataframe.replace('\-$', '0', regex=True, inplace=True)
    return dataframe


def get_column_data_type(dataframe: pd.DataFrame):
    column_data_type = {}

    for column in dataframe.columns:
        if column in ['종목코드', ('종목코드', '')]:
            continue
        for data in dataframe[column]:
            if data == 0 or data == '':
                continue
            try:
                data = eval(data)
            except:
                pass
            data_type = type(data)
            if data_type is str:
                break
            elif data_type is int:
                column_data_type[column] = 'np.int64'
            elif data_type is float:
                column_data_type[column] = 'float'
    return column_data_type


def data_type_as(dataframe: pd.DataFrame, column_data_type: dict):
    for column_name in column_data_type:
        dataframe = dataframe.astype({column_name: eval(column_data_type[column_name])})
    return dataframe