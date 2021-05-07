CoreDotFinance.Crypto.Binance
=============================

CoreDotFinance 내에서 암호화화폐 데이터를 제공하는 라이브러리 입니다.

현재  제공하고 있는 데이터는 binance.com 에서 가져고오 있습니다.

사용방법
--------
import coredotfinance.crypto.binance as coin

# Binance 암호화화폐 Ticker 리스트 조회
coin.get_ticker()

# 대상 Ticker 일자별 OHLCV 데이터 조회
df = coin.get_crypto_ohlcv(ticker, interval, start, end, limit)

# 대상 Ticker 일자별 OHLCV 데이터로 그래프 그리기
graph = coin.make_ohlcv_graph(df)
