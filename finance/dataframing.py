# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime

second_column_map = {
    'BND_CLSS_NM1': '구분1',  # <- row map
    'BND_CLSS_NM2': '구분2',  # <- row map
}

no_display_columns = ['IND_TP_CD', 'IDX_IND_CD', 'MKT_ID',
                      'CONV_OBJ_TP_CD', 'ISU_ABBRV_STR', 'ETF_ISU_CD',
                      'BND_CLSS_CD', 'NUSUAL_ISU_COND_CONTN',
                      'KRW_FLUC_TP_CD', 'OZ_FLUC_TP_CD', 'FLUC_TP',
                      'ISU_ABBRV', 'SUB_IDX_IND_NM', 'ISU_CD']


class Data_nm:
    _data_nm = None
    def __init__(self):
        pass

    @property
    def data_nm(self):
        item_name = Data_nm._data_nm
        Data_nm._data_nm = None
        return item_name

    @data_nm.setter
    def data_nm(self, item_name):
        Data_nm._data_nm = item_name


def to_dataframe(data_json, column_map):
    data_validation(data_json)
    data = apply_column_map(data_json, column_map)
    data = date_to_index(data)
    data = multi_columnize(data)
    data = string_to_float(data)
    data = data_nm_column(data)
    return data


def data_validation(data_json):
    if len(list(data_json.values())[0]) == 0:
        raise Exception("No data, Check parameters")


def apply_column_map(data_json, column_map):
    global second_column_map
    column_map.update(second_column_map)
    readable_column_list = []
    # ignored = set()  # delete later
    only_key = list(data_json.keys())[0]
    data_list = data_json[only_key]
    for data in data_list:
        readable_column = {}
        for column, data_value in data.items():
            try:
                readable_column[column_map[column]] = data_value
            except:
                if column in no_display_columns or 'TP_CD' in column:
                    # ignored.add(column)
                    continue
                readable_column[column] = data_value
        readable_column_list.append(readable_column)
    # print(f'ignored{ignored}')
    return pd.json_normalize(readable_column_list)

def multi_columnize(data):
    column_data = [column.split("//") for column in data.columns]
    columns_depth = max([len(c) for c in column_data])
    # columns 가 single 인 경우
    if columns_depth == 1:
        return data
    columns = []
    # 같은 이름으로 multi columnize 되는 것을 방지
    for i in column_data:
        for _ in range(columns_depth - len(i)):
            i.append('')
    # column 만들기
    for i in range(1, columns_depth + 1):
        layer = []
        for column in column_data:
            layer.append(column[:i][-1])
        columns.append(layer)
    data.columns = columns
    return data

def remove_recursive_column_name(columns):
    pass


def string_to_float(data):
    new_values = []
    for column in data.columns:
        series = data[column]
        edited_values = []
        number_data = True
        for i in series:
            try:
                value = float(i.replace(',', ''))
            except:
                if i != '-':
                    number_data = False
                    break
                else:
                    value = np.nan
            edited_values.append(value)
        if number_data:
            new_values.append(edited_values)
        else:
            new_values.append(series.array)

    return pd.DataFrame(np.array(new_values).T, columns=data.columns, index=data.index)


def date_to_index(data):
    if '일자' not in data.columns:
        # '일자' 열이 있는지 확인
        return data
    if len(data) != len(set(data['일자'].values)):
        # '일자' 가 중복되는 데이터인지 확인
        return data

    date_list = [datetime.strptime(date, '%Y/%m/%d') for date in data['일자']]
    data.index = date_list
    return data.drop(['일자'], axis='columns')


def data_nm_column(data):
    item_name = Data_nm().data_nm
    if item_name is None:
        return data
    data['종목명'] = [item_name for _ in range(len(data))]

    return data


