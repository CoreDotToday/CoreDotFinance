# -*- coding: utf-8 -*-
import pandas as pd

col_map = {
    'IDX_NM': '지수명',
    'CLSPRC_IDX': '종가',
    'FLUC_TP_CD': '증감',
    'CMPPREVDD_IDX': '대비',
    'FLUC_RT': '등락률',
    'OPNPRC_IDX': '시가',
    'HGPRC_IDX': '고가',
    'LWPRC_IDX': '저가',
    'ACC_TRDVOL': '거래량',
    'ACC_TRDVAL': '거래대금',
    'MKTCAP': '상장시가총액'
}


def convert_key(data):
    converted = []
    for d in data['output']:
        new = {}
        for k, v in d.items():
            new[col_map[k]] = v
        converted.append(new)
    return pd.json_normalize(converted)

