# finance
 http://data.krx.co.kr 의 데이터를 Python library로 쉽게 사용한다.
 #  사용법
 ## 1. 지수
 #### 1.1 주가 지수

 ```python
 import coredotfinance

 # 전체 지수 시세 11001
 data = coredotfinance.data_reader('11001', day=20210121, division='kospi')

 # 전체 지수 변동률 11002
 data = coredotfinance.data_reader('11002', start=20210101, end=20210121, division='kospi')

 # 개별 지수 시세추이 1103
 data = coredotfinance.data_reader('11003', start=20210101, end=20210121, ind_name='코스피 200')

 # 전체 지수 기본 정보 11004
 data = coredotfinance.data_reader('11004', division='kospi)

 # 개별 지수 종합 정보 11005
 pass

 # 지수 구성 목록 11006
 data = coredotfinance.data_reader('11006', day=20210121, ind_name='코스피 200')

 #전체지수 PER/PBR/배당수익률 11007_a
 data = coredotfinance.data_reader('11006', day=20210121, divison='kospi')

 # 개별지수 PER/PBR/배당수익률 11007_b
 data = coredotfinance.data_reader('11006', start=20210101, end=20210121, ind_name='코스피 200')
 ```
 #### 1.2 채권 지수
 ```python
 import coredotfinance
 # 전체 지수 시세 11008
 data = finanace.data_reader('11008', day=20210121)

 # 개별 지수 시세 추이 11009
 data = coredotfinance.data_reader('11009', start=20210101, end=20210121, bond='KRX채권지수') 
 ```
 #### 1.3 파생 및 기타지수
 ```python
 import coredotfinance
 pass
 ```

 ## 2. 주식
 #### 2.1 종목시세
 #### 2.2 종목정보
 #### 2.3 거래실적
 #### 2.4 기타증권
 #### 2.5 세부안내
 ```python
 import coredotfinance
 # PER/PBR/배당수익률(개별종목) [12021]
 #   전종목 검색
 data = coredotfinance.data_reader('12021', division='kospi', search_type='전종목', day=20210101)
 #   개별추이/종목명 검색
 data = coredotfinance.data_reader('12021', division='kospi', search_type = '개별추이', start=20210101, end=20210201, stk_name='삼성바이오로직스')
 #   개별추이/종목코드 검색
 data = coredotfinance.data_reader('12021', division='kospi', search_type = '개별추이', start=20210101, end=20210201, stk_code='207940')
 ```

 ## 4. 채권

 #### 4.1 종목시세

 ```python
 import coredotfinance
 # [14001] 전종목 시세 
 data = coredotfinance.data_reader('14001', day=20210317, market="소액채권시장")

 # [14002] 개별종목 시세 추이
 data = coredotfinance.data_reader('14002', start=20210216, end=20210316, market="국채전문유통시장", product="국고01125-2509(20-6)")
 ```

 #### 4.2 종목정보

 ```python
 import coredotfinance
 # [14003] 전종목 기본정보
 data = coredotfinance.data_reader('14003', bond_type="국채")

 # [14004] 개별종목 종합정보
 pass
 ```

 #### 4.3 거래실적

 # 사용법
 ### 종목검색
 ```python
 import coredotfinance
 # [14005] 종류별 거래 실적
 data = coredotfinance.data_reader('14005', start=20210309, end=20210316, market="일반채권시장", inquiry="채권유형별")

 # [14006] 투자자별 거래실적
 data = coredotfinance.data_reader('14006', start=20210309, end=20210316, market="소액채권시장")
 # 전종목 시세검색
 coredotfinance.get()

 # [14007] 국채지표종목 거래실적
 data = coredotfinance.data_reader('14007', start=20210309, end=20210316)
 # 종목명 시세검색
 data = coredotfinance.get('삼성전자', 20200101, 2021101)

 # [14008] Repo 거래실적
 data = coredotfinance.data_reader('14008', start=20210309, end=20210316)
 # 종목코드 시세검색
 data = coredotfinance.get('001120', 20200101, 2021101)
 ```

 #### 4.4 세부안내

 `coredotfinance.get('종목명 또는 종목코드', '검색 시작일', '검색 종료일')`
 ### 종목 per/pbr/배당수익률 검색
 ```python
 import coredotfinance
 # [14009] 개별종목 시가평가 추이
 data = coredotfinance.data_reader('14009', start=20210216, end=20210316, product="국고01125-2509(20-6)", inquiry="발표일")

 # [14010] 소액채권 신고가격 추이
 data = coredotfinance.data_reader('14010', start=20210310, end=20210317)

 # [14011] 상장채권 상세검색
 data = coredotfinance.data_reader('14011', product="AJ네트웍스", bond_type="회사채")

 # [14012] 상장채권 발행정보
 data = coredotfinance.data_reader('14012', product="서울도시철도21-03")

 # [14013] 상장유형별 내역
 data = coredotfinance.data_reader('14013', start=20210216, end=20210316, inquiry="추가", bond_type="특수채")

 # [14014] 상장금액조정 내역
 data = coredotfinance.data_reader('14014', start=20210216, end=20210316)

 # [14015] 중도상환
 data = coredotfinance.data_reader('14015', start=20210216, end=20210316, inquiry="중도상환(전액)")

 # [14016] 채권상장폐지
 data = coredotfinance.data_reader('14016', start=20200316, end=20210316, inquiry="상장폐지")

 # inquiry="전종목"
 data = coredotfinance.data_reader('14017', inquiry="전종목", day=20210310)

 # inquiry="개별추이"
 # bond_type: 채권종류
 data = coredotfinance.data_reader('14017', inquiry="개별추이", bond_type="국고채 3년", start=20210217, end=20210317)

 # [14018] 지표수익률
 data = coredotfinance.data_reader('14018', start=20210217, end=20210317)

 # [14019] 스트립 단기금리
 data = coredotfinance.data_reader('14019', start=20210217, end=20210317, inquiry="15:30 기준")

 # [14020] 채권 대용가 --> 미작동

 # inquiry="전종목"  --> 미작동
 data = coredotfinance.data_reader('14020', start=20210317, end=20210317, inquiry="전종목")

 # inquiry="개별추이"  --> 미작동
 # product: 종목명 (코드 입력 X)
 data = coredotfinance.data_reader('14020', start=20210217, end=20210317, product="울산지역개발21-02")

 # [14021] 발행기관별 채권 대용가
 # product: 발행기관명 (코드 입력 X)
 data = coredotfinance.data_reader('14021', start=20210309, end=20210317, product="울산시")

 # [14022] 유형별 채권 대용가
 data = coredotfinance.data_reader('14022', start=20210309, end=20210317, bond_type="회사채", inquiry="카드채권")
 # 전종목 per/pbr/배당수익률 검색
 coredotfinance.per()

 # [14023] 발행기관별 신용등급
 data = coredotfinance.data_reader('14023', start=20210309, end=20210317, product="산업은행", inquiry="한국신용평가")
 # 종목명 per/pbr/배당수익률 검색
 data = coredotfinance.per('삼성전자', 20200101, 20210101)

 # [14024] 신용등급별 상장현황
 data = coredotfinance.data_reader('14024', day=20210317, inquiry="NICE신용평가")
 # 종목코드 per/pbr/배당수익률 검색
 data = coredotfinance.per('001120', 20200101, 20210101)

 # [14025] 전환사채 투자지표
 data = coredotfinance.data_reader('14025', day=20210316)

 # [14026] 주식관련채권 권리행사
 data = coredotfinance.data_reader('14026', start=20210309, end=20210317, product="HMM199CB")

 # [14027] 주식관련채권 행사가액
 data = coredotfinance.data_reader('14027', start=20190316, end=20210317)
 ```

 ## 5. 파생상품

 #### 5.1 종목시세

 ```python
 import coredotfinance
 # [15001] 전종목 시세
 data = coredotfinance.data_reader('15001', day=20210317, item="코스피200 옵션", market="call")

 # [15002] 개별종목 시세 추이 
 data = coredotfinance.data_reader('15002', start=20210309, end=20210317, item="코스피200 C 202104 262.5")

 # [15003] 최근월물 시세 추이(선물) --> 상품구분에 따른 상세선택 항목 없음(예: 섹터지수 선물 선택시 상세선택 활성화됨)
 data = coredotfinance.data_reader('15003', start=20210309, end=20210317, item="코스피200 선물", market="정규")
 ```

 #### 5.2 종목정보

 ```python
 import coredotfinance
 # [15004] 전종목 기본정보  --> 상품구분에 따른 상세선택 항목 없음(예: 섹터지수 선물 선택시 상세선택 활성화됨)
 data = coredotfinance.data_reader('15004', item="코스피200 선물")

 # [15005] 개별종목 종합정보
 pass
 ```

 #### 5.3 거래실적

 ```python
 import coredotfinance
 # [15006] 전체상품 거래실적
 data = coredotfinance.data_reader('15006', day=20210316)

 # [15007] 투자자별 거래실적 --> 일부 미작동, 상세선택 및 권리유형 미구현
 # inquiry="기간합계"
 data = coredotfinance.data_reader('15007', start=20210309, end=20210316, item="코스피200 옵션", search_type="기간합계")
 # inquiry="일별추이"
 data = coredotfinance.data_reader('15007', start=20210309, end=20210316, item="코스닥150 선물", search_type="일별추이", trade_index="거래량", trade_check="매수")

 # [15008] 협의대량거래실적 추이 --> 상세선택 및 권리유형 미구현
 data = coredotfinance.data_reader('15008', start=20210309, end=20210316, item="코스피200 선물")

 # [15009] 기초자산별 거래실적(주식선물/옵션)
 data = coredotfinance.data_reader('15009', start=20210309, end=20210316, item="주식선물")
 data = coredotfinance.data_reader('15009', start=20210309, end=20210316, item="주식옵션", right_type="CALL")
 ```

 #### 5.4 세부안내

 ```python
 import coredotfinance
 # [15010] 베이시스 추이(선물)  --> 일부 제대로 작동 안함

 # inquiry="상품" --> 상세선택 미구현
 data = coredotfinance.data_reader('15010', start=20210309, end=20210316, search_type="상품", item="10년국채 선물", detail="최근월물")

 # inquiry="개별종목"
 data = coredotfinance.data_reader('15010', start=20210309, end=20210316, search_type="개별종목", item="변동성지수 F 202109")

 # [15011] 내재변동성 추이(옵션)
 data = coredotfinance.data_reader('15011', start=20210216, end=20210316, item="미니코스피200 옵션")

 # [15012] P/C Ratio 추이(옵션)
 data = coredotfinance.data_reader('15012', start=20210216, end=20210316, item="코스피200 위클리 옵션")

 # [15013] 행사가격/만기별 가격표(옵션)
 pass

 # [15014] 돈육시세 동향

 # 아래 표
 data = coredotfinance.data_reader('15014', start=20210216, end=20210316, inquiry="현재가")

 # 위 표
 data = coredotfinance.data_reader('15014', start=20210216, end=20210316)

 # [15015] 최종결제가격 급변
 # 기간별조회만 가능, 월별로 조회(day 중 연월 정보만으로 조회)
 data = coredotfinance.data_reader('15015', day=20210217, inquiry="매수")

 # [15016] 낮은 권리행사 비율
 # 기간별조회만 가능, 월별로 조회(day 중 연월 정보만으로 조회)
 data = coredotfinance.data_reader('15016', start=20210117, end=20210317)
 ```

 ## 6. 일반상품

 #### 6.1 석유

 ```python
 import coredotfinance
 # [16101] 전종목 기본정보
 data = coredotfinance.data_reader('16101', oil="휘발유")

 # [16102] 유종별 시세 추이
 data = coredotfinance.data_reader('16102', start=20210309, end=20210316, oil="등유")

 # [16103] 참가자별 거래실적

 # inquiry="기간합계"
 data = coredotfinance.data_reader('16103', start=20210309, end=20210316, oil="경유", inquiry="기간합계")

 # inquiry="일별추이"  --> 오류 수정 완료
 data = coredotfinance.data_reader('16103', start=20210309, end=20210316, oil="경유", inquiry="일별추이", trade_index="거래량", trade_check="매도")

 # [16104] 국내유가(주유소) 동향
 data = coredotfinance.data_reader('16104', start=20210309, end=20210316, oil="휘발유")
 ```

 #### 6.2 금

 ```python
 import coredotfinance
 # [16201] 전종목 시세
 data = coredotfinance.data_reader('16201', day=20210317)

 # [16202] 개별종목 시세 추이
 data = coredotfinance.data_reader('16202', start=20210309, end=20210317, gold="미니금 100g")

 # [16203] 전종목 기본정보
 data = coredotfinance.data_reader('16203')

 # [16204] 개별종목 종합정보 
 pass

 # [16205] 투자자별 거래실적

 # inquiry="기간합계"  
 data = coredotfinance.data_reader('16205', start=20210309, end=20210316, inquiry="기간합계")

 # inquiry="일별추이"  --> 오류 수정 완료
 data = coredotfinance.data_reader('16205', start=20210309, end=20210316, inquiry="일별추이", trade_index="거래대금", trade_check="매수")

 # [16206] 협의대량거래실적 추이
 data = coredotfinance.data_reader('16206', start=20210309, end=20210316)

 # [16207] 국제금시세 동향

 # 아래 표
 data = coredotfinance.data_reader('16207', start=20210309, end=20210316)

 # 위 표  --> 이용불가능
 data = coredotfinance.data_reader('16207', start=20210309, end=20210316, inquiry="현재가")
 ```

 #### 6.3 배출권

 ```python
 import coredotfinance
 # [16301] 전종목 시세
 data = coredotfinance.data_reader('16301', day=20210317)

 # [16302] 개별종목 시세 추이
 data = coredotfinance.data_reader('16302', start=20210309, end=20210317, item="KAU21")

 # [16303] 전종목 기본정보
 data = coredotfinance.data_reader('16303')

 # [16304] 개별종목 종합정보
 pass
 ```

 ## 7. 해외연계시장

 #### 7.1 EUREX

 ```python
 import coredotfinance
 # [17101~17103] 미구현

 # [17104] 개별종목 시세 추이
 data = coredotfinance.data_reader('17104', start=20210216, end=20210316, right_type="PUT")

 # [17105] 권리유형별 거래실적 추이(월)
 # start와 end의 연월 data만 활용하여 검색
 data = coredotfinance.data_reader('17105', start=20210216, end=20210316, right_type="전체")

 # [17106] 만기별 가격표(옵션)
 # day의 연월 data만 활용하여 검색
 data = coredotfinance.data_reader('17106', day=20210417) # 미래의 월 입력

 # [17107] 주요통계 추이
 pass

 # [17108] EURO STOXX 50 시세 추이
 data = coredotfinance.data_reader('17108', start=20201216, end=20210316)
 ```

 #### 7.2 동경거래소 시세

 ```python
 import coredotfinance
 # [17109] 개별종목 종합정보
 pass
 ```


