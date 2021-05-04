# 사용법

## Package Import
```python
import coredotfinance.crypto as coin
```

## Binance 암호화화폐 Ticker 리스트 조회
```python
coin.get_ticker()
```

## 대상 Ticker 일자별 OHLCV 데이터 조회
```python
data = coin.get_kline_candlestick_data('BTCUSDT')
df = coin.convert_candle_to_dataframe(data)
df
```

## 대상 Ticker 일자별 OHLCV 데이터로 그래프 그리기
```python
coin.make_ohlcv_graph(df)
```