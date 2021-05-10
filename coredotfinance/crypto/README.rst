CoreDotFinance.Crypto.Binance
=============================

CoreDotFinance 내에서 암호화화폐 데이터를 제공하는 라이브러리 입니다.

현재  제공하고 있는 데이터는 binance.com 에서 가져고오 있습니다.

사용방법
--------
::

    import coredotfinance.crypto as coin

    # Binance 암호화화폐 Ticker 리스트 조회
    coin.get_tickers()

    # 대상 Ticker 현재 가격 조회
    coin.get_current_price(ticker)

    # 대상 Ticker 호가 조회
    coin.get_orderbook(ticker)

    # 대상 Ticker 현재 상세정보 조회
    coin.get_market_detail(ticker)

    # USD 기준 전체 Ticker 최근 24시간 기준 가격 조회
    coin.get_24hrs()

    # 대상 Ticker Historical OHLCV(시가, 고가, 저가, 종가, 거래량) 데이터 조회
    coin.get_ohlcv(ticker, interval, start, end, limit)
    df = coin.get_ohlcv()  # default 값(ticker: 'BTCBUSD', interval: '1d', start/end: 최근날짜, limit=500)
    df = coin.get_ohlcv('ethbusd', interval='1h')

    # 대상 Ticker Historical OHLCV 데이터로 그래프 그리기
    graph = coin.make_ohlcv_graph(df)

.. code-block:: python
