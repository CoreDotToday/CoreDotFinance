# -*- coding: utf-8 -*-
import pandas as pd

second_column_map = {
    'BND_CLSS_NM1': '구분1',  # <- row map
    'BND_CLSS_NM2': '구분2',  # <- row map
}

no_display_columns = ['IND_TP_CD', 'IDX_IND_CD', 'MKT_ID',
                      'CONV_OBJ_TP_CD', 'ISU_ABBRV_STR', 'ETF_ISU_CD',
                      'BND_CLSS_CD', 'NUSUAL_ISU_COND_CONTN',
                      'KRW_FLUC_TP_CD', 'OZ_FLUC_TP_CD', 'FLUC_TP']

def convert(data_json, column_map):
    global second_column_map
    column_map.update(second_column_map)
    readable_column_list = []
    not_in_map = set()  # delete later
    ignored = set()  # delete later
    only_key = list(data_json.keys())[0]
    data_list = data_json[only_key]
    for data in data_list:
        readable_column = {}
        for column, data_value in data.items():
            try:
                readable_column[column_map[column]] = data_value
                # readable_column[column] = data_value  # In order to check origin column name
            except:
                if column in no_display_columns or 'TP_CD' in column:
                    ignored.add(column)
                    continue
                readable_column[column] = data_value
                not_in_map.add(column)  # delete try except no need to use
        readable_column_list.append(readable_column)
    print(f'ignored{ignored}')
    return pd.json_normalize(readable_column_list)

