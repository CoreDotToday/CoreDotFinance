.. currentmodule:: coredotfinance

CoreDotFinance
===============
Version : 1.0.0

**Core.Today**: `https://core.today <https://core.today>`__

**CoreDotFinance**: `https://github.com/CoreDotToday/CoreDotFinance <https://github.com/CoreDotToday/CoreDotFinance>`__

금융 데이터를 쉽고 빠르게
-------------------

**CoreDotFinance** 는 데이터를 쉽고 빠르게 사용할 수 있게 도와주는 파이썬 라이브러리입니다.
한국의 금융데이터는 **Krx**, 가상 화폐 데이터는 **binance** 에서 받아옵니다.
대용량 데이터의 경우 CoreDotFinance 만의 api를 이용해서 사용할 수 있습니다.

**KRX**: `https://data.krx.co.kr <https://data.krx.co.kr>`__

**Binance** `https://binance.com <https://binance.com>`__


Quick Start
-----------

``pip install coredotfinance`` 를 통해서 라이브러리를 설치할 수 있습니다.

.. code-block:: shell

   pip install coredotfinance

- KrxReader Example

.. code-block:: python

   from coredotfinance.data import KrxReader
   # symbol '005930' stands for Samsung
   krx = KrxReader()
   krx.read('005930', start='2021-06-03', end='2021-06-06')

- BinanceReader Example

.. code-block:: python

   from coredotfinance.data import BinanceReader
   # symbol 'BTCUSDT' stands for Bitcoin
   binance = BinanceReader()
   binance.read('BTCUSDT', start = '2021-06-04', end = '2021-07-01', interval = '1h')

Contents
--------
.. panels::
   :card: + intro-card text-center

   ---
   :img-top: _static/krx.png

   **KRX**

   Krx 는 한국의 금융 데이터를 다루는 온라인 웹사이트 입니다.
   CoreDotFinance 를 통해서 주식, ETF, 주식배당금 등의 다양한 데이터를 이용해서 나만의 포트폴리오를 작성해보세요.
   Krx 데이터는 `data.krx.co.kr <https://data.krx.co.kr>`__ 에서 불러옵니다.

   +++

   .. link-button:: krx_example
            :type: ref
            :text: Krx Data
            :classes: bot-block btn-outline-primary

   ---
   :img-top: _static/binance.svg

   **Binance**

   Binance 는 가상화폐 데이터를 다루는 온라인 웹사이트 입니다.
   CoreDotFinance 를 통해 가상화폐 데이터를 이용해서 화쳬 가격의 동향을 예측해보세요.
   binance 데이터는 `binance.com <https://www.binance.com>`__ 에서 불러옵니다.

   +++

   .. link-button:: binance_documentation 
            :type: ref
            :text: Binance Data
            :classes: bot-block btn-outline-primary


.. toctree::
   :maxdepth: 1

Recent developments
-------------------
You can install the latest development version using

.. code-block:: shell

   pip install git+https://github.com/CoreDotToday/CoreDotFinance.git

or

.. code-block:: shell

   git clone https://github.com/CoreDotToday/CoreDotFinance.git
   cd CoreDotToday
   python setup.py install



Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :maxdepth: 1

   krx_documentation.rst
