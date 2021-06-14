CoreDotFinance
====================================

.. image:: https://img.shields.io/github/stars/CoreDotToday/CoreDotFinance
    :target: https://github.com/CoreDotToday/CoreDotFinance
    :alt: stars

.. image:: https://img.shields.io/github/issues/CoreDotToday/CoreDotFinance
    :target: https://github.com/CoreDotToday/CoreDotFinance/issues
    :alt: issues

`CoreDotFinance` 는 주가, 지표, 파생상품, 비트코인 등 금융 데이터를 제공하는 라이브러리입니다.
현재 제공하고 있는 데이터는 data.krx.co.kr 에서 가져오고 있습니다.
비트코인 데이터를 준비하고 있습니다.

사용방법
------
::

    $ git clone https://github.com/CoreDotToday/CoreDotFinance.git
    $ cd CoreDotFinance
    $ python setup.py install


.. code-block:: python

Documentation
---------------
The official documentation is hosted on https://coredottoday.github.io/CoreDotFinance/


get
--------
krx 주식 데이터
::

    import coredotfinance.krx as krx

    # 전종목 종합 검색 (최근 2달치)
    data = krx.get()

    # 전종목 종합 검색
    data = krx.get('all', 20210101, 20210401)

    # 개별 종목 가격 검색 (종목명)
    data  = krx.get('삼성전자', 202100101, 20210401)

    # 종목코드 시세 검색 (종목코드)
    data = krx.get('001120', 202100101, 20210401)

.. code-block:: python

per
--------
krx per 데이터
::
    import coredotfinance.krx as krx

    # 전종목 per/ pbr/ 배당수익 검색
    data = krx.per()

    # 전종목 per/ pbr/ 배당수익 검색
    data = krx.per('all', 20210101, 20210401)

    # 개별종목 per/ pbr/ 배당수익 검색 (종목명)
    data = krx.per('삼성전자', 202100101, 20210401)

    # 개별종목 per/ pbr/ 배당수익 검색 (종목코드)
    data = krx.per('001120', 202100101, 20210401)

.. code-block:: python

etf
--------
krx etf 데이터
::
    import coredotfinance.krx as krx

    # 전종목 etf 검색
    data = krx.etf()

    # 전종목 etf 검색
    data = krx.etf('all', 20210101, 20210401)

    # 개별종목 etf 검색 (종목명)
    data = krx.etf('arirang 200', 202100101, 20210401)

    # 개별종목 etf 검색 (종목코드)
    data = krx.etf('152100', 202100101, 20210401)

.. code-block:: python



etn
--------
krx etn 데이터
::
    import coredotfinance.krx as krx

    # 전종목 etn 검색
    data = krx.etn()

    # 전종목 etn 검색
    data = krx.etf('all', 20210101, 20210401)

    # 개별종목 etn 검색 (종목명)
    data = krx.etn('KB KRX300 ETN', 202100101, 20210401)

    # 개별종목 etn 검색 (종목코드)
    data = krx.etn('550060', 202100101, 20210401)

.. code-block:: python



elw
--------
krx elw 데이터
::
    import coredotfinance.krx as krx

    # 전종목 elw 검색
    data = krx.elw()

    # 전종목 etn 검색
    data = krx.elw('all', 20210101, 20210401)

    # 개별종목 elw 검색 (종목명)
    data = krx.elw('KBF937삼성전자콜', 202100101, 20210401)

    # 개별종목 elw 검색 (종목코드)
    data = krx.elw('58F937', 202100101, 20210401)

.. code-block:: python






