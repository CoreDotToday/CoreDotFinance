# 사용법
### 종목검색
```python
import finance

# 전종목 시세검색
finance.get()

# 종목명 시세검색
data = finance.get('삼성전자', 20200101, 2021101)

# 종목코드 시세검색
data = finance.get('001120', 20200101, 2021101)
```
`finance.get('종목명 또는 종목코드', '검색 시작일', '검색 종료일')`
### 종목 per/pbr/배당수익률 검색
```python
import finance
# 전종목 per/pbr/배당수익률 검색
finance.per()

# 종목명 per/pbr/배당수익률 검색
data = finance.per('삼성전자', 20200101, 20210101)

# 종목코드 per/pbr/배당수익률 검색
data = finance.per('001120', 20200101, 20210101)

```
`finance.per('종목명 또는 종목코드', '검색 시작일', '검색 종료일')`