CoreDotFinance
====================================

`CoreDotFinance`는 주가, 지표, 파생상품, 비트코인 등 금융 데이터를 제공하는 라이브러리입니다.

현재 제공하고 있는 데이터는 data.krx.co.kr 에서 가져오고 있습니다.

비트코인 데이터를 준비하고 있습니다.

사용방법
------
::

    $ git clone https://github.com/CoreDotToday/CoreDotFinance.git
    $ cd CoreDotFinance
    $ python setup.py install


.. code-block:: python


get
--------
krx 주식 데이터
::

    import coredotfinance as cdf

    # 전종목 시세 검색
    data = cdf.get()

    # 종목명 시세 검색
    data  = cdf.get('삼성전자', 202100101, 20210401)

    # 종목코드 시세 검색
    data = cdf.get('001120', 202100101, 20210401)

.. code-block:: python

per
--------
krx per 데이터
::
    import coredotfinance as cdf

    # 전종목 per/ pbr/ 배당수익 검색
    data = cdf.per()

    # 종목명 per/ pbr/ 배당수익 검색
    data = cdf.per('삼성전자', 202100101, 20210401)

    # 종목코드 per/ pbr/ 배당수익 검색
    data = cdf.per('001120', 202100101, 20210401)

.. code-block:: python

etf
--------
krx etf 데이터
::
    import coredotfinance as cdf

    # 전종목 etf 검색
    data = cdf.etf()

    # 종목명 etf 검색
    data = cdf.etf('arirang 200', 202100101, 20210401)

    # 종목코드 etf 검색
    data = cdf.etf('152100', 202100101, 20210401)

.. code-block:: python



etn
--------
krx etn 데이터
::
    import coredotfinance as cdf

    # 전종목 etn 검색
    data = cdf.etn()

    # 종목명 etn 검색
    data = cdf.etn('KB KRX300 ETN', 202100101, 20210401)

    # 종목코드 etn 검색
    data = cdf.etn('550060', 202100101, 20210401)

.. code-block:: python



elw
--------
krx elw 데이터
::
    import coredotfinance as cdf

    # 전종목 elw 검색
    data = cdf.elw()

    # 종목명 elw 검색
    data = cdf.elw('KBF937삼성전자콜', 202100101, 20210401)

    # 종목코드 elw 검색
    data = cdf.elw('58F937', 202100101, 20210401)

.. code-block:: python






