# -*- coding: utf-8 -*-
import pandas as pd

col_map = {
    'IDX_NM': '지수명',
    'IDX_IND_NM': '지수명',
    'IDX_ENG_NM': '지수영문명',
    'BAS_DD': '일자',
    'BAS_TM_CONTN': '기준일',
    'ANNC_TM_CONTN': '발표일',
    'BAS_IDX_CONTN': '기준지수',
    'CALC_CYCLE_CONTN': '산출지수',
    'CALC_TM_CONTN': '산출시간',
    'COMPST_ISU_CNT': '구성족목수',
    'ISU_SRT_CD': '종목코드',
    'ISU_ABBRV': '종목명',
    'OPN_DD_INDX': '시작일기준',
    'END_DD_INDX': '종료일기준',
    'TRD_DD': '일자',
    'CLSPRC_IDX': '종가',
    'TDD_CLSPRC': '종가',
    'FLUC_TP_CD1': '총수익증감',
    'FLUC_TP_CD2': '순가격증감',
    'FLUC_TP_CD3': '제로투자증감',
    'FLUC_TP_CD4': '콜재투증감',
    'FLUC_TP_CD5': '시장가격증감',
    'FLUC_TP_CD': '증감',
    'CMPPREVDD_IDX': '대비',
    'CMPPREVDD_IDX1': '총수익대비',
    'CMPPREVDD_IDX2': '순가격대비',
    'CMPPREVDD_IDX3': '제로투자대비',
    'CMPPREVDD_IDX4': '콜재투자대비',
    'CMPPREVDD_IDX5': '시장가격대비',
    'FLUC_TP': '대비',
    'PRV_DD_CMPR': '대비',
    'STR_CMP_PRC' : '대비',
    'UPDN_RATE': '등락률',
    'FLUC_RT': '등락률',
    'OPNPRC_IDX': '시가',
    'HGPRC_IDX': '고가',
    'LWPRC_IDX': '저가',
    'ACC_TRDVOL': '거래량',
    'ACC_TRDVAL': '거래대금',
    'MKTCAP': '상장시가총액',
    'WT_PER': 'PER',
    'WT_STKPRC_NETASST_RTO': 'PBR',
    'DIV_YD': '배당수익률',
    'BND_IDX_GRP_NM': '지수명',
    'TOT_EARNG_IDX': '총수익종가',
    'TOT_EARNG_IDX_FLUC_TP': '총수익증감',
    'TOT_EARNG_IDX_CMPPREVDD': '총수익대비',
    'NETPRC_IDX': '순가격종가',
    'NETPRC_IDX_FLUC_TP': '순가격증감',
    'NETPRC_IDX_CMPPREVDD': '순가격대비',
    'ZERO_REINVST_IDX': '제로재투자종가',
    'ZERO_REINVST_IDX_FLUC_TP': '제로재투자증감',
    'ZERO_REINVST_IDX_CMPPREVDD': '제재투자대비',
    'CALL_REINVST_IDX': '콜재투자지수',
    'CALL_REINVST_IDX_FLUC_TP': '콜재투자증감',
    'CALL_REINVST_IDX_CMPPREVDD': '콜재투대비',
    'MKT_PRC_IDX': '시장가격지수',
    'MKT_PRC_IDX_FLUC_TP': '시장가격증감',
    'MKT_PRC_IDX_CMPPREVDD': '시장가격대비',
    'AVG_DURATION': '듀레이션',
    'AVG_CONVEXITY_PRC': '컨벡시티',
    'BND_IDX_AVG_YD': 'YTM'
}


def convert(data):
    converted = []
    not_in_map = set() # delete later
    for d in data['output']:
        new = {}
        for k, v in d.items():
            try:
                new[col_map[k]] = v
            except:
                if k in ['IND_TP_CD', 'IDX_IND_CD']:
                    continue
                new[k] = v
                not_in_map.add(k) # delete try except no need to use
        converted.append(new)
    print(not_in_map)
    return pd.json_normalize(converted)

