import pandas as pd
import numpy as np
from coredotfinance.krx.data_reader_ import *
from coredotfinance.krx.utils_moon import *


def convert_stock_ticker_name(stock: str) -> str:
    """
    '종목코드'(6자리)를 입력하면 '종목명' 반환, '종목명'을 입력하면 '종목코드'를 반환
    """
    stock_list = get_stock_info().loc[:,['종목코드', '종목명']]
    def convert_stock_ticker2name(stock_ticker: str) -> str:
        stock_name = stock_list[stock_list['종목코드'] == stock_ticker]['종목명'].array[0]
        return stock_name

    def convert_stock_name2ticker(stock_name: str) -> str:
        stock_ticker = stock_list[stock_list['종목명'] == stock_name]['종목코드'].array[0]
        return stock_ticker

    if stock in stock_list['종목코드'].array:
        return convert_stock_ticker2name(stock)
    elif stock in stock_list['종목명'].array:
        return convert_stock_name2ticker(stock)


def get_stock_info() -> pd.DataFrame:
    """
    KRX(KOSPI ,KOSDAQ) 종목 정보 반환
    """
    df_12025_kospi = data_reader('12025', division='KOSPI').loc[:, ['종목코드', '종목명', '시장구분', '업종명', '시가총액']]
    df_12025_kosdaq = data_reader('12025', division='KOSDAQ').loc[:, ['종목코드', '종목명', '시장구분', '업종명', '시가총액']]
    df_12025 = (
        pd
        .concat([df_12025_kospi, df_12025_kosdaq])
        .astype({'시장구분':'category', '시가총액':'int64'})
        .sort_values(by=['시가총액'], ascending=False)
        .reset_index(drop=True)
    )
    df_12025.index = np.arange(1, len(df_12025) + 1)  # index 1부터 시작하도록 맞추기
    return df_12025


def get_stock_pack(stock: str=None, start: str=get_past_days_ago(), end: str=get_today()) -> pd.DataFrame:
    """
    주어진 기간의 일자별 개별종목의 정보들을 합쳐 하나의 데이터프레임으로 가져온다.
    KRX 정보데이터시스템 통계 메뉴 중
    - 합쳐진 개별종목 정보 -> [12003] 개별종목 시세 추이, [12021] PER/PBR/배당수익률(개별종목), [12023] 외국인보유량(개별종목), [12009] 투자자별 거래실적(개별종목)
    - 향후 업데이트 예정 -> , [31001] 개별종목 공매도 종합정보
    Parameters
    ----------
    stock : str
        종목번호(ticker) 또는 종목명
    start : str, default : 오늘 날짜의 60일 전 날짜
        데이터 검색 시작 일자 (예: 20210324)
    end : str, default : 오늘 날짜
        데이터 검색 끝 일자 (예: 20210407)
    Returns
    -------
    pandas.dataframe
        KRX 정보데이터시스템의 개별종목 정보들을 합쳐놓은 DataFrame 반환
    """
    stock_list = get_stock_info().loc[:,['종목코드', '종목명']]
    if stock in stock_list['종목코드'].array:
        item = convert_stock_ticker_name(stock)
        item_code = stock
    elif stock in stock_list['종목명'].array:
        item = stock
        item_code = convert_stock_ticker_name(stock)

    # [12003] 개별종목 시세 추이
    df_12003 = data_reader('12003', item=item, start=start, end=end)
    # [12021] PER/PBR/배당수익률(개별종목)
    df_12021 = data_reader('12021', search_type='개별추이', item=item, start=start, end=end)
    # [12023] 외국인보유량(개별종목)
    df_12023 = data_reader('12023', search_type='개별추이', item=item, start=start, end=end)
    # [12009] 투자자별 거래실적(개별종목)
    def get_df_12009(item=item, start=start, end=end):
        """
        거래량/거래대금 * 매도/매수/순매수 = 총 6개의 표의 상세보기 포함 정보를 하나의 DataFrame으로 합쳐서 반환
        Parameters
        ----------
        item : str
            pack() 함수의 parameter인 stock이 종목명일 때 종목명을 가져옴
        item_code : str
            pack() 함수의 parameter인 stock이 종목코드일 때 종목코드를 가져옴
        start : str
            pack() 함수의 parameter인 start 일자를 가져옴
        end : str
            pack() 함수의 parameter인 end 일자를 가져옴
        Returns
        -------
        DataFrame
            개별종목의 투자자별 거래실적 상세 항목을 모두 포함한 DataFrame 반환
        """
        trdvolval_list = ['거래량', '거래대금']  # trdVolVal {1: '거래량', 2: '거래대금'}
        askbid_list = ['순매수']  # askBid {1: '매도', 2: '매수', 3: '순매수'}
        dfs = []
        for trdvolval in trdvolval_list:
            for askbid in askbid_list:
                df_temp = data_reader('12009', item=item, start=start, end=end,
                                      search_type='일별추이', trade_index=trdvolval, trade_check=askbid)
                df_temp.drop(['종목명'], axis='columns', inplace=True)  # 매 번 반복되는 종목명 column 제거
                col_name = f'{trdvolval}-{askbid}'
                df_temp.columns = pd.MultiIndex.from_product([[col_name], df_temp.columns])
                dfs.append(df_temp)
        df = pd.concat(dfs, axis='columns')
        return df
    df_12009 = get_df_12009(item=item)

    print('< 일자별 개별종목 종합정보 조회 >')
    print(f'종목명: {item} // 종목코드: {item_code} // 조회기간: {start}~{end}')
    df = pd.concat([df_12003, df_12021, df_12023, df_12009], axis="columns")  # DataFrame을 Columns 기준으로 합침
    df = (df
          .loc[:, ~df.columns.duplicated()]  # 중복되는 Columns 제외
          .sort_index(ascending=False)  # 최신 날짜가 위로 올라오도록 정렬
          )
    return df


def get_adjusted_price(df: pd.DataFrame, col: str, *, inplace: bool=False) -> pd.Series:
    """
    DataFrame의 최근 일자의 상장주식수와 동일하도록 다른 날짜의 상장주식수를 수정하여 각 날짜별 수정 가격 Column을 반환
    Parameters
    ----------
    df : DataFrame
        수정 가격을 적용할 DataFrame
    col : str
        수정 가격을 적용할 원본 가격 Column 이름 ('종가', '시가', '고가', '저가')
    inplace : boolean, default = False
        원본 DataFrame에 '수정'이라는 이름을 앞에 붙인 Column을 추가하는 옵션
    Returns
    -------
    Series
        수정 가격이 적용된 Column(Series)
    Examples
    --------
    adjusted_price = get_adjusted_price(df, '종가')
    """
    if col in ['종가', '시가', '고가', '저가', '거래량']:
        latest_stocks = df['상장주식수'][df.index == df.index.max()].array[0]  # DataFrame의 최근 일자의 상장주식수
        adjusted_price = (df[col] * (df['상장주식수'] / latest_stocks)).astype(np.int32)  # 수정 가격
        if col in ['거래량']:
            adjusted_price = (df[col] / (df['상장주식수'] / latest_stocks)).astype(np.int32)  # 수정 거래량
        if inplace:
            df[f'수정{col}'] = adjusted_price  # 원본 DataFrame에 '수정'이라는 이름을 앞에 붙인 Column을 추가 (기본값=False)
        return adjusted_price
    else:
        print("올바른 Column을 선택해주세요. (선택가능 Column: '종가', '시가', '고가', '저가', '거래량'")