# import os
import datetime
import pandas as pd
import numpy as np
from finance import data_reader


def get_today():
    today = datetime.date.today()
    return today.strftime('%Y%m%d')


def get_past_days_ago(days: int=60) -> str:
    today = datetime.date.today()
    past_days_ago = today - datetime.timedelta(days)
    return past_days_ago.strftime('%Y%m%d')


# dir = os.path.dirname(os.path.realpath(__file__))
# stock_list = pd.read_csv(dir + '/info_stock_list.csv')  # 종목코드, 종목명, 시장구분, 업종명, 시가총액
# pack() 함수에서 {start}의 초기 값을 14로 만들어, 날짜 정보 미입력시 '오늘로부터 14일 전~오늘'의 데이터를 조회할 수 있도록 만듦


def get_df(data: dict) -> pd.DataFrame:
    """
    data_reader 함수로 가져올 수 없는 KRX 통계를 가져올 수 있도록 만듦
    Parameters
    ----------
    data : dict
        getJsonData.cmd에 입력하는 Form Data를 dict 형식으로 입력받음
    Returns
    -------
    DataFrame
    """
    from finance.statistics.basic.info import Info
    from finance.dataframing import to_dataframe
    get_basic_statistics = Info(start=None, end=None, day=None)
    data_json, column_map = get_basic_statistics.requests_data(data)
    df = to_dataframe(data_json, column_map)
    return df


def get_df_12020() -> pd.DataFrame:
    """
    [12020] 상장회사 상세검색
    Returns
    -------
    DataFrame
        KRX 정보데이터시스템의 '[12020] 상장회사 상세검색' 메뉴에서 전체 조회를 한 화면의 DataFrame 리턴
    """
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT03402',
        'mktTpCd': '전체',
        'isuSrtCd': 'ALL',
        'isuSrtCd2': 'ALL',
        # 'sortType': 'A',
        # 'stdIndCd': 'ALL',
        # 'sectTpCd': 'ALL',
        # 'parval': 'ALL',
        # 'mktcap': 'ALL',
        # 'acntclsMm': 'ALL'
    }
    df = get_df(data)
    # 종목코드와 업종코드의 형식을 맞춤
    df['종목코드'] = df['종목코드'].apply(lambda x: make_6digits_code(x))
    df['업종코드'] = df['업종코드'].apply(lambda x: make_6digits_code(x))
    return df


def get_df_12025() -> pd.DataFrame:
    # [12025] 업종분류 현황 (KOSPI, KOSDAQ)
    df_12025_kospi = data_reader('12025', division='KOSPI').iloc[:, [0, 1, 2, 3, -1]]
    df_12025_kosdaq = data_reader('12025', division='KOSDAQ').iloc[:, [0, 1, 2, 3, -1]]
    df_12025 = pd.concat([df_12025_kospi, df_12025_kosdaq])
    return df_12025


stock_list = get_df_12025()
print(stock_list)

def make_6digits_code(code: float) -> str:
    """
    종목코드/업종코드 등의 코드를 6자리 형식으로 맞추어줌
    (예: '5930.0' -> '005930')
    """
    return f'{float(code):06.0f}'


def get_stock(stock: str) -> str:
    """
    종목코드를 입력하면 종목명 반환, 종목명을 입력하면 종목코드를 반환
    Parameters
    ----------
    stock : str
        종목코드 6자리(0포함) 또는 종목명
    Returns
    -------
    str
        종목코드 입력 -> 종목명 반환
        종목명 입력 -> 종목코드 반환
    """
    def get_stock_name(stock_ticker: str) -> str:
        stock_name = stock_list[stock_list['종목코드'] == stock_ticker]['종목명'].array[0]
        return stock_name

    def get_stock_ticker(stock_name: str) -> str:
        stock_ticker = stock_list[stock_list['종목명'] == stock_name]['종목코드'].array[0]
        return stock_ticker

    if stock in stock_list['종목코드'].array:
        return get_stock_name(stock)
    elif stock in stock_list['종목명'].array:
        return get_stock_ticker(stock)


def get_adjusted_price(df: pd.DataFrame, col: pd.Series, *, inplace: bool=False) -> pd.Series:
    """
    DataFrame의 최근 일자의 상장주식수와 동일하도록 다른 날짜의 상장주식수를 수정하여 각 날짜별 수정 가격 Column을 반환
    Parameters
    ----------
    df : DataFrame
        수정 가격을 적용할 DataFrame
    col : Series
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


def info(kind: str='주식', *, sort: str='종목명', ascending: bool=True, outfile: bool=False) -> pd.DataFrame:  # * 이후는 키워드만 사용 가능
    """
    주식 관련 종합 정보 조회 (KOSPI, KOSDAQ)
    KONEX는 제외
    Parameters
    ----------
    kind : str, default = '주식'
        '주식' : 전체 주식 기본 정보 조회 (KOSPI, KODEX)
        '상장회사' : 상장회사 전체 조회 ('KOSPI, KOSDAQ, KONEX')
    sort : str, default = '종목명'
        정렬 기준 column명 지정
    ascending : bool, default = True (오름차순)
        정렬 기준 오름차순(True)/내림차순(False) 지정
    outfile : boolean, default = False
        True : DataFrame을 csv 파일로 저장
    Returns
    -------
    DataFrame
        최종 DataFrame 리턴
    """
    if kind == '주식':
        # [12025] 업종분류 현황 (KOSPI, KOSDAQ)
        df_12025 = get_df_12025()
        # [12005] 전종목 기본정보
        df_12005 = data_reader('12005', division='전체').set_index('단축코드')  # concat을 위해 index를 종목코드로 맞춰줌
        # [12006] 전종목 지정내역
        df_12006 = data_reader('12006', division='전체').set_index('종목코드')  # concat을 위해 index를 종목코드로 맞춰줌
        df = pd.concat([df_12025, df_12005, df_12006], axis='columns')
        df = (df
              .loc[:, ~df.columns.duplicated()]  # 중복되는 Columns 제외
              .dropna()  # df_12025의 종목명을 기준으로 쓰면서 결측값이 돼버린 KONEX 종목 삭제
              .sort_values(by=sort, ascending=ascending)  # 종목명 기준으로 정렬
              .reset_index().rename(columns={'index': '종목코드'})  # concat을 위해 index로 사용했던 '종목코드' 원상태로 복귀
              )
        df.index = np.arange(1, len(df) + 1)  # index 1부터 시작하도록 맞추기
        if len(df_12025) == len(df):  # KOSPI/KOSDAQ 종목 개수가 맞는 지 확인 후 개수 일치하면 df 반환
            if outfile:  # 전체 조회는 자주 변하지 않지만 data 양이 많으므로 매번 crawling 하는 것 보다 파일로 저장해서 관리하고자 함
                # df.to_csv('info_stock.csv')
                df_stock_list = df.loc[:, ['종목코드', '종목명', '시장구분', '업종명', '시가총액']]
                df_stock_list.to_csv('info_stock_list.csv')

            print('< 전체 주식 기본 정보 조회 (KOSPI, KOSDAQ) >')
            return df
        else:
            print('뭔가 잘못됐다....')
    elif kind == '상장회사':  # publicly listed company
        # [12020] 상장회사 상세검색 (KOSPI, KOSDAQ) -> 상장 종목 개수 > 상장 회사 개수
        df = get_df_12020()
        df = (df
                [df['시장구분'] != 'KONEX']  # 'stock'과 동일하게 KONEX 제외
                .sort_values(by=sort, ascending=ascending)  # 정렬 기준 파라마미터 정의
                .reset_index(drop=True)  # index 번호 reset
                )
        df.index = np.arange(1, len(df) + 1)  # index 1부터 시작하도록 맞추기
        if outfile:  # 전체 조회는 자주 변하지 않지만 data 양이 많으므로 매번 crawling 하는 것 보다 pkl 파일로 저장해서 관리하고자 함
            df.to_csv('info_listed_company.csv')
        print('< 상장회사 전체 조회 (KOSPI, KOSDAQ) >')
        return df


def pack(stock: str=None, start: str=get_past_days_ago, end: str=get_today) -> pd.DataFrame:
    """
    주어진 기간의 일자별 개별종목의 정보들을 합쳐 하나의 데이터프레임으로 가져온다.
    KRX 정보데이터시스템 통계 메뉴 중
    - 합쳐진 개별종목 정보 -> [12003] 개별종목 시세 추이, [12021] PER/PBR/배당수익률(개별종목), [12023] 외국인보유량(개별종목), [12009] 투자자별 거래실적(개별종목)
    - 향후 업데이트 예정 -> , [31001] 개별종목 공매도 종합정보, [32001] 개별종목 공매도 거래
    Parameters
    ----------
    stock : str
        종목번호(ticker) 또는 종목명
    start : int or str, default : 오늘 날짜의 14일 전 날짜
        데이터 검색 시작 일자 (예: 20210324)
    end : int or str, default : 오늘 날짜
        데이터 검색 끝 일자 (예: 20210407)
    Returns
    -------
    pandas.dataframe
        KRX 정보데이터시스템의 개별종목 정보들을 합쳐놓은 DataFrame 반환
    """
    if stock in stock_list['종목코드'].array:
        item = get_stock(stock)
        item_code = stock
    elif stock in stock_list['종목명'].array:
        item = stock
        item_code = get_stock(stock)

    # [12003] 개별종목 시세 추이
    # df_12003 = data_reader('12003', item=item, item_code=item_code, start=start, end=end)

    # [12021] PER/PBR/배당수익률(개별종목)
    # df_12021 = data_reader('12021', search_type='개별추이', item=item, item_code=item_code, start=start, end=end)

    # [12023] 외국인보유량(개별종목)
    # df_12023 = data_reader('12023', search_type='개별추이', item=item, item_code=item_code, start=start, end=end)

    # [12009] 투자자별 거래실적(개별종목)
    def get_df_12009(item: str=item, item_code: str=item_code, start: str=start, end: str=end) -> pd.DataFrame:
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
        askbid_list = ['매도', '매수', '순매수']  # askBid {1: '매도', 2: '매수', 3: '순매수'}
        dfs = []
        for trdvolval in trdvolval_list:
            for askbid in askbid_list:
                df_temp = data_reader('12009', item=item, item_code=item_code, start=start, end=end,
                                      search_type='일별추이', trade_index=trdvolval, trade_check=askbid, detail='상세보기')
                df_temp.drop(['종목명'], axis='columns', inplace=True)  # 매 번 반복되는 종목명 column 제거
                col_institutional_investor = ['금융투자', '보험', '투신', '사모', '은행', '기타금융', '연기금 등']
                col_foreign_investor = ['외국인', '기타외국인']
                df_temp['기관 합계'] = df_temp.loc[:, col_institutional_investor].sum(axis='columns')
                df_temp['외국인 합계'] = df_temp.loc[:, col_foreign_investor].sum(axis='columns')
                col_new = ['금융투자', '보험', '투신', '사모', '은행', '기타금융', '연기금 등', '기관 합계', '기타법인', '개인',
                           '외국인', '기타외국인', '외국인 합계', '전체']
                df_temp = df_temp[col_new]  # '기간 합계'와 '외국인 합계' 열 위치 조정
                col_name = f'{trdvolval}-{askbid}'
                df_temp.columns = pd.MultiIndex.from_product([[col_name], df_temp.columns])
                dfs.append(df_temp)
        df = pd.concat(dfs, axis='columns')
        return df
    df_12009 = get_df_12009(item=item)
    # [31001] 개별종목 공매도 종합정보, [32001] 개별종목 공매도 거래 -> 업데이트 예정 (아직 공매도 통계 미구현 -> 먼 미래)
    print('< 일자별 개별종목 종합정보 조회 >')
    print(f'종목명: {item} // 종목코드: {item_code} // 조회기간: {start}~{end}')
    df = pd.concat([df_12003, df_12021, df_12023, df_12009], axis="columns")  # DataFrame을 Columns 기준으로 합침
    df = (df
          .loc[:, ~df.columns.duplicated()]  # 중복되는 Columns 제외
          .sort_index(ascending=False)  # 최신 날짜가 위로 올라오도록 정렬
          )
    return df
# stock_list = get_df_12025().loc[:, ['종목코드', '종목명', '시장구분', '업종명']]
# print(stock_list['종목코드'])
pack('두산퓨얼셀')
# print(stock_list)